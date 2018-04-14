import math

from numpy import pi, exp, fft, sin, ones, array, zeros, arange, absolute, transpose, concatenate
from matplotlib import pyplot as plt

from ionospheredata.calc import pmap, linspace


def main():
    b16 = 2**16
    x_arg = linspace(0, 10, 1000)
    y_arg = sin(1.6 * pi * x_arg)  # 1.6 = 2 * 8 / 10

    gca = plt.subplot(2, 2, 1)
    plt.plot(x_arg, y_arg, 'b')
    plt.grid(True)
    gca.set_xlim(xmax=max(x_arg), xmin=0)

    # fft by
    y_long = concatenate((transpose(y_arg), zeros((b16 - y_arg.shape[0]))), axis=0)

    nfft = b16
    ftto = fft.fft(y_long, n=nfft, axis=0)
    gca = plt.subplot(2, 2, 2)
    plt.plot(arange(0, nfft, 1), absolute(ftto), 'b')
    plt.grid(True)
    gca.set_xlim(xmax=30, xmin=0)

    # Spectr Spread

    y1_arg = exp((x_arg - ones(x_arg.shape) * -5 * 10**-9 * b16 / 2) ** 2) * sin(x_arg * 2 * 8 * pi / b16)

    gca = plt.subplot(2, 2, 3)
    plt.plot(x_arg, y1_arg, 'b')
    plt.grid(True)
    gca.set_xlim(xmin=0, xmax=max(x_arg))

    # fft by
    y1_long = concatenate((transpose(y_arg), zeros((b16 - y_arg.shape[0]))), axis=0)

    nfft = b16
    ftto1 = fft.fft(y1_long, n=nfft, axis=0)

    gca = plt.subplot(2, 2, 4)
    plt.plot(arange(0, nfft, 1), absolute(ftto1), 'b')
    plt.grid(True)
    gca.set_xlim(xmax=30, xmin=0)

    plt.show()

if __name__ == '__main__':
    main()
