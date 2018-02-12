# from numpy import bartlett
# from numpy import blackman
# from numpy import convolve
# from numpy import hamming
# from numpy import hanning
# from numpy import ones
# from numpy import r_

# __SMOOTHING_METHODS = {
#     'hanning': hanning,
#     'hamming': hamming,
#     'bartlett': bartlett,
#     'blackman': blackman,
# }
from numpy import array


def smooth(x, window_len=11):
    result = []
    w2 = window_len // 2
    l = len(x)
    for i in range(l):
        db = min(i, w2)
        dt = min(l - 2 - i, w2 - 1)
        d = min(db, dt)
        sub_seq = x[i - d:i + d + 1]
        # print((i, ws, we, sum(sub_seq), len(sub_seq), sum(sub_seq) / len(sub_seq) if len(sub_seq) else 0))
        if i == l - 1:
            result.append(x[i])
        if len(sub_seq) == 0:
            result.append(0)
        else:
            result.append(sum(sub_seq) / (2 * d + 1))
    return array(result)

# def smooth(x, window_len=11, window='hanning'):
#     """Source: http://scipy-cookbook.readthedocs.io/items/SignalSmooth.html
#     Smooth the data using a window with requested size.

#     This method is based on the convolution of a scaled window with the signal.
#     The signal is prepared by introducing reflected copies of the signal
#     (with the window size) in both ends so that transient parts are minimized
#     in the begining and end part of the output signal.

#     input:
#         x: the input signal
#         window_len: the dimension of the smoothing window; should be an odd integer
#         window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
#             flat window will produce a moving average smoothing.

#     output:
#         the smoothed signal

#     example:

#     t=linspace(-2,2,0.1)
#     x=sin(t)+randn(len(t))*0.1
#     y=smooth(x)

#     see also:

#     numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
#     scipy.signal.lfilter

#     TODO: the window parameter could be the window itself if an array instead of a string
#     NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
#     """

#     if len(x.shape) != 1:
#         raise ValueError('smooth only accepts 1 dimension arrays.')

#     if len(x) < window_len:
#         raise ValueError('Input vector needs to be bigger than window size.')


#     if window_len < 3:
#         return x


#     if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
#         raise ValueError('Window is on of \'flat\', \'hanning\', \'hamming\', \'bartlett\', \'blackman\'')


#     s = r_[x[window_len - 1 : 0 : -1], x, x[-2 : -window_len - 1 : -1]]
#     if window == 'flat':  # moving average
#         w = ones(window_len, 'd')
#     else:
#         w = __SMOOTHING_METHODS[window](window_len)

#     return convolve(w / w.sum(), s, mode='valid')
