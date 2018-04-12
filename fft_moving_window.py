from numpy import arange, ones, concatenate, zeros, transpose
from numpy.fft import fft
from matplotlib import pyplot as plt


def main():
    y_arg = concatenate((ones((72, )), zeros((1642, ))), axis=0)

    gca = plt.subplot(2, 2, 1)
    plt.plot(y_arg, 'b')
    plt.grid(True)
    gca.set_xlim(xmin=0, xmax=y_arg.shape[0])

    # fft by 
    b16 = 2**16
    y_long = concatenate((transpose(y_arg), zeros((b16 - y_arg.shape[0]))), axis=0)

    nfft = b16
    ffto = fft(y_long, nfft) / 72;

    gca = plt.subplot(2,2,2)
    plt.plot(arange(0, nfft, 1), ones((nfft, )) - ffto)
    plt.grid(True)
    gca.set_xlim(xmin=0, xmax=2600)

    plt.show()


    # 11 signal points = 85 km
    # for j=1:11
    #     y1(j)=1;
    # end
    #     for j=length(y1)+1:1642
    #         y1(j)=0;
    #     end

    # subplot(2,2,3), plot(y1,'r','LineWidth',2); grid on
    # set(gca,'XLim',[0 length(y1)]);

    # % fft by 
    # y1_long = [y1';zeros(2^16-length(y1),1)];
    #     FFTO1 = fft(y1_long,nfft)/11;

    # subplot(2,2,4), plot(1:nfft,(1-ffto(1:nfft)).*FFTO1(1:nfft),'r','LineWidth',2); grid on
    # set(gca,'XLim',[0 2600]);


if __name__ == '__main__':
    main()
