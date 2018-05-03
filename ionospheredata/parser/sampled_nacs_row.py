from collections import OrderedDict

from .row_parser import RowParser


class SampledNACSRow(RowParser):
    seed = [
        OrderedDict([
            ('ut', ((0, 15), float)),
            ('o_dens', ((15, 29), float)),  # +6, +7
            ('o_err', ((29, 37), float)),  # +8
            ('n2_dens', ((37, 51), float)),  # +9
            ('n2_err', ((51, 59), float)),  # +10
            ('he_dens', ((59, 73), float)),  # +11
            ('he_err', ((73, 81), float)),  # +12
            ('n_dens', ((81, 95), float)),  # +13
            ('n_err', ((95, 103), float)),  # +14
            ('ar_dens', ((103, 117), float)),  # +15
            ('ar_err', ((117, 125), float)),  # +16
            ('orbit', ((125, 132), int)),  # +17
            ('alt', ((132, 141), float)),  # +18
            ('lat', ((141, 150), float)),  # +19
            ('lon', ((150, 159), float)),  # +20
            ('lst', ((159, 166), float)),  # +21
            ('lmt', ((166, 173), float)),  # +22
            ('l_sh', ((173, 182), float)),  # +23
            ('inv_lat', ((182, 191), float)),  # +24
            ('sza', ((191, 199), float)),  # +25
        ])
    ]
    filename = OrderedDict([
        ('year', ((0, 4), int)),
        ('day_of_year', ((4, 7), int)),
    ])
    drop_lines = 0
