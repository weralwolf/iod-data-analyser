from colored import bg, fg, attr, stylize


def _make_color_function(color):
    def wrapped(msg):
        return stylize(msg, color)
    return wrapped


noticeRed = _make_color_function(fg(256) + bg(9) + attr('bold'))
noticeGreen = _make_color_function(fg(256) + bg(76) + attr('bold'))
noticeYellow = _make_color_function(fg(256) + bg(208) + attr('bold'))


red = _make_color_function(fg(9) + bg(0) + attr('bold'))
green = _make_color_function(fg(76) + bg(0) + attr('bold'))
yellow = _make_color_function(fg(208) + bg(0) + attr('bold'))
