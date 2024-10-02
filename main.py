import ezdxf.math
import matplotlib.pyplot as plt
import numpy as np
import shapely
import ezdxf

# Constants
RESOLUTION = 100  # number of points per waveform
REVCYCLES = 50  # number of surface cycles per revolution of the wheel
RADIUS = 20  # nominal radius of the wheel, mm
AMPLITUDE = RADIUS * 0.05  # amplitude of the surface
WAVETYPE = "sqr"  # type of wave to use
WAVES = ["sin", "saw", "sqr", "hill", "tri"]  # valid wave types
FILENAME = f"DXFS/tonewheel_{WAVETYPE}_r{RADIUS}_{REVCYCLES}T.dxf"
SHOWDEMO = False


def create_domain(domain: float) -> np.ndarray:
    return np.arange(0, domain, domain / (REVCYCLES * RESOLUTION))


def create_wave(domain: np.ndarray, wave_type: str) -> np.ndarray:
    match wave_type:
        case "sin":
            return np.sin(domain)
        case "hill":
            return np.abs(np.sin(domain / 2)) * 2 - 1
        case "saw":
            return np.mod(domain, 2 * np.pi) / (np.pi) - 1
            # return domain - np.floor()
        case "sqr":
            return np.sign(np.sin(domain))
        case "tri":
            return np.arcsin(np.sin(domain))
        case "flat":
            return np.ones_like(domain)
        case _:
            raise ValueError("Invalid wave type")


def create_polar_plot(theta, r, plot: plt.axes = None):
    # use polar coordinates to plot
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    if plt is None:
        plt.plot(x, y)
    else:
        plt.plot(x, y)
    # set aspect ratios to be equal on polar plots
    plot.set_aspect("equal", "box")


def create_tonewheel_profile_array(wave: str = WAVETYPE) -> np.ndarray:
    # create domain
    theta = create_domain((np.pi * 2))
    wave = create_wave(REVCYCLES * theta, wave)
    r = RADIUS + AMPLITUDE * wave
    polar = np.array([theta, r])
    # convert to cartesian
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return np.array([x, y]).T


def create_tonewheel_tooth_array(wave: str = WAVETYPE) -> np.ndarray:
    # create domain
    theta = np.arange(
        0, (np.pi * 2) / REVCYCLES, ((np.pi * 2) / REVCYCLES) / RESOLUTION
    )
    theta = np.arange(0, (np.pi * 2), (np.pi * 2) / RESOLUTION)
    wave = create_wave(REVCYCLES * theta, wave)
    r = RADIUS + AMPLITUDE * wave
    polar = np.array([theta, r])
    # convert to cartesian
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return np.array([x, y]).T


def create_tonewheel_profile_dxf(arr: np.ndarray, filename: str = "tonewheel.dxf"):
    # shape = shapely.geometry.Polygon(arr)
    # create dxf
    doc = ezdxf.new()
    msp = doc.modelspace()
    msp.add_lwpolyline(arr, close=True)
    # msp.add_spline(arr)
    # spline = ezdxf.math.fit_points_to_cad_cv(arr)
    # msp.add_shape(spline)
    # msp.add_lwpolyline(create_hole(5.75), close=True)
    msp.add_circle(center=(0, 0), radius=5.75 / 2)
    msp.add_point((0, 0))
    doc.saveas(filename)


def create_tonewheel_tooth_profile_dxf(
    arr: np.ndarray, filename: str = "tonewheel_tooth.dxf"
):
    doc = ezdxf.new()
    msp = doc.modelspace()
    msp.add_lwpolyline(arr, close=False)
    msp.add_circle(center=(0, 0), radius=5.75 / 2)
    msp.add_point((0, 0))
    doc.saveas(filename)


def show_demo(waves: list[str] = WAVES):
    # create domain
    theta = create_domain(np.pi * 2)

    fig = plt.figure(layout="constrained")
    fig.suptitle("Tonewheel Profiles")
    fig.set_size_inches(4, 1.5 * len(waves))
    subfigs: np.ndarray[plt.figure] = fig.subfigures(len(waves), 1)

    for i in range(len(waves)):
        axs = subfigs[i].subplots(1, 3)
        subfigs[i].suptitle(waves[i])
        wave = create_wave(REVCYCLES * theta, waves[i])
        r = RADIUS + AMPLITUDE * wave
        # shorten x to just 3 cycles
        x = theta[: int(len(theta) / REVCYCLES) * 3]
        wave = wave[: int(len(x))]
        axs[0].plot(x, wave)
        create_polar_plot(theta, r, axs[2])
        arr = create_tonewheel_tooth_array()
        arr = create_tonewheel_profile_array()
        print(arr)
        axs[1].plot(arr)

    plt.show()


if __name__ == "__main__":
    if SHOWDEMO:
        show_demo()
    arr = create_tonewheel_profile_array()
    # plt.plot(arr)
    # plt.show()
    create_tonewheel_profile_dxf(arr, FILENAME)
    print("Produced Tonewheel File")
    # tooth = create_tonewheel_tooth_array()
    # create_tonewheel_tooth_profile_dxf(tooth)
