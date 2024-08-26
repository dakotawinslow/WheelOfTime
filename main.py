import matplotlib.pyplot as plt
import numpy as np

# Constants
RESOLUTION = 0.01
REVCYCLES = 20  # number of surface cycles per revolution of the wheel
RADIUS = 1  # nominal radius of the wheel
AMPLITUDE = 0.1  # amplitude of the surface
WAVETYPE = "saw"  # type of wave to use
WAVES = ["sin", "saw", "sqr", "hill", "tri"]  # valid wave types


def create_domain(domain: float) -> np.ndarray:
    return np.arange(0, domain, RESOLUTION)


def create_wave(domain: np.ndarray, wave_type: str) -> np.ndarray:
    match wave_type:
        case "sin":
            return np.sin(domain)
        case "hill":
            return np.abs(np.sin(domain))
        case "saw":
            return np.mod(domain, 2 * np.pi) / np.pi - 1
        case "sqr":
            return np.sign(np.sin(domain))
        case "tri":
            return np.arcsin(np.sin(domain))
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


if __name__ == "__main__":
    # create domain
    theta = create_domain(np.pi * 2 + RESOLUTION)
    x = theta
    #  create wave
    wave = create_wave(REVCYCLES * theta, WAVETYPE)
    # create r
    r = RADIUS + AMPLITUDE * wave

    fig = plt.figure(layout="constrained")
    fig.suptitle("Tonewheel Profiles")
    fig.set_size_inches(4, 1.5 * len(WAVES))
    subfigs: np.ndarray[plt.figure] = fig.subfigures(len(WAVES), 1)

    for i in range(len(WAVES)):
        axs = subfigs[i].subplots(1, 2)
        subfigs[i].suptitle(WAVES[i])
        wave = create_wave(REVCYCLES * theta, WAVES[i])
        r = RADIUS + AMPLITUDE * wave
        # shorten x to just 3 cycles
        x = theta[: int(len(theta) / REVCYCLES) * 3]
        wave = wave[: int(len(x))]
        axs[0].plot(x, wave)
        create_polar_plot(theta, r, axs[1])

    plt.show()
