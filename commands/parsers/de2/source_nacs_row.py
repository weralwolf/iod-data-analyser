from typing import List
from collections import OrderedDict
from commands.parsers.row_parser import RowParser


class SourceNACSRow(RowParser):
    seed: List[OrderedDict] = [
        OrderedDict([
            ('ut', ((0, 9), int)),
            ('o_dens', ((9, 22), float)),
            ('o_err', ((22, 29), float)),
            ('n2_dens', ((29, 42), float)),
            ('n2_err', ((42, 49), float)),
            ('he_dens', ((49, 62), float)),
            ('he_err', ((62, 69), float)),
            ('n_dens', ((69, 82), float)),
            ('n_err', ((82, 89), float)),
            ('ar_dens', ((89, 102), float)),
            ('ar_err', ((102, 109), float)),
            ('orbit', ((109, 115), int)),
            ('alt', ((115, 123), float)),
            ('lat', ((123, 131), float)),
            ('lon', ((131, 139), float)),
            ('lst', ((139, 145), float)),
            ('lmt', ((145, 151), float)),
            ('l_sh', ((151, 159), float)),
            ('inv_lat', ((159, 167), float)),
            ('sza', ((167, 174), float)),
        ])
    ]
    filename: OrderedDict = OrderedDict([
        ('year', ((0, 4), int)),
        ('day_of_year', ((4, 7), int)),
    ])
    drop_lines: int = 2
