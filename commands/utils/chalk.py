from typing import Callable

from colored import bg, fg, attr, stylize


def _make_color_function(color: str) -> Callable:
    def wrapped(msg: str) -> str:
        return str(stylize(msg, color))
    return wrapped


noticeRed = _make_color_function(fg(255) + bg(9) + attr('bold'))
noticeGreen = _make_color_function(fg(255) + bg(76) + attr('bold'))
noticeYellow = _make_color_function(fg(255) + bg(208) + attr('bold'))


red = _make_color_function(fg(9) + bg(0))
red_bold = _make_color_function(fg(9) + bg(0) + attr('bold'))
green = _make_color_function(fg(28) + bg(0))
green_bold = _make_color_function(fg(76) + bg(0) + attr('bold'))
yellow = _make_color_function(fg(208) + bg(0))
yellow_bold = _make_color_function(fg(208) + bg(0) + attr('bold'))
dim_grey = _make_color_function(fg(241) + bg(0) + attr('dim'))
dim_light_grey = _make_color_function(fg(251) + bg(0) + attr('dim'))
