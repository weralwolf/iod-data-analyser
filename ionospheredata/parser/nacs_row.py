from collections import OrderedDict

from .row_parser import RowParser


class NACSRow(RowParser):
    seed = [
        OrderedDict([
            ('ut', (0, 9)),
            ('o_dens', (9, 22)),
            ('o_err', (22, 29)),
            ('n2_dens', (29, 42)),
            ('n2_err', (42, 49)),
            ('he_dens', (49, 62)),
            ('he_err', (62, 69)),
            ('n_dens', (69, 82)),
            ('n_err', (82, 89)),
            ('ar_dens', (89, 102)),
            ('ar_err', (102, 109)),
            ('orbit', (109, 115)),
            ('alt', (115, 123)),
            ('lat', (123, 131)),
            ('lon', (131, 139)),
            ('lst', (139, 145)),
            ('lmt', (145, 151)),
            ('l_sh', (151, 159)),
            ('inv_lat', (159, 167)),
            ('sza', (167, 174)),
        ])
    ]
    drop_lines = 2
