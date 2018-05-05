from collections import OrderedDict

from .row_parser import RowParser


class SampledNACSRow(RowParser):
    seed = [
        OrderedDict([
            ('ut', ((0, 15), float)),
            ('o_dens', ((15, 30), float)),
            ('o_err', ((30, 38), float)),
            ('n2_dens', ((38, 53), float)),
            ('n2_err', ((53, 61), float)),
            ('he_dens', ((61, 76), float)),
            ('he_err', ((76, 84), float)),
            ('n_dens', ((84, 99), float)),
            ('n_err', ((99, 107), float)),
            ('ar_dens', ((108, 122), float)),
            ('ar_err', ((122, 130), float)),
            ('orbit', ((130, 137), int)),
            ('alt', ((137, 146), float)),
            ('lat', ((146, 155), float)),
            ('lon', ((155, 164), float)),
            ('lst', ((164, 171), float)),
            ('lmt', ((171, 178), float)),
            ('l_sh', ((178, 187), float)),
            ('inv_lat', ((187, 196), float)),
            ('sza', ((196, 204), float)),
        ])
    ]
    filename = OrderedDict([])
    drop_lines = 0
