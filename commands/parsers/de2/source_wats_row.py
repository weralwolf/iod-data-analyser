from typing import List
from collections import OrderedDict
from commands.parsers.row_parser import RowParser


class SourceWATSRow(RowParser):
    seed: List[OrderedDict] = [
        OrderedDict([
            ('year', ((1, 3), int)),
            ('day', ((3, 6), int)),
            # 1 - date   (I5)    [yyddd]
            ('ut', ((6, 15), int)),
            # 2 - UT         (I9)    [ms]
            ('mode', ((15, 17), int)),
            # 3 - Mode   (I2)        =3,4 measuring the horizontal velocity
            #             =5,6 measuring the vertical velocity
            ('slot', ((17, 18), int)),
            # 4 - Slot   (I1)        =1,2,3,4; steps from 1 to 4 during each 8-sec
            #             measurement sequence, mode may change at each
            #             step.
            ('outin', ((18, 19), int)),
            # 5 - Outin  (I1)        =1 baffle going out, =0 going in
            ('mass', ((19, 22), int)),
            # 6 - Mass   (I3)    [AMU]   Usually 28 or 32 (32 is assume to be mostly
            #             atomic oxygen which is recombined in the
            #             instrument).
            ('density', ((22, 34), float)),
            # 7 - Density    (E12.5) [cm-3]  Density of neutrals with mass given in Word 6
            #             (negative values should be ignored).
            ('tn', ((34, 41), float)),
            # 8 - Tn     (F7.1)  [K] Neutral temperature of neutral with mass given
            #             in word 6.
            ('tn_corr', ((41, 48), float)),
            # 9 - Tn_corr*   (F7.1)  [K] Neutral temperature after WATSCOR correction.
            ('v_sc', ((48, 56), float)),
            # 10 - V_s/c      (F8.1)  [m/s]   Horizontal (zonal) velocity (of neutrals with
            #                 mass given in word 5) if Mode=3,4. Velocity is
            #                 given in spacecraft spacecraft coordinates
            #                 (positiv in the Z-axis direction).
            #                 Vertical velocity in s/c coordinates (positive
            #                 in the Y axis direction) if Mode=5,6.
            ('c1', ((56, 62), int)),
            # 11 - C1**   (1X,I5)     (Instrument counts)/8
            ('c2', ((62, 67), int)),
            # 12 - C2     (I5)        (Counts + background)/8
            ('t1', ((67, 71), int)),
            # 13 - T1***  (1X,I3) [2s/255] Time when the baffle crosses the first optical
            #                 position sensor.
            ('t2', ((71, 74), int)),
            # 14 - T2***  (I3)    [2s/255] Time when the baffle crosses the second optical
            #                 position sensor.
        ]),
        OrderedDict([
            #   -121.2  -121.2    77  363.6 -39.3  145.2  1.50  1.90-9.00  51.4  149.8
            ('v_geo', ((0, 9), float)),
            # 15 - V_geo  (/F8.1) [m/s]   Horizontal/vertical (zonal) velocity in
            #                 corotating Earth frame (positive in
            #                 the eastward/upward direction) if
            #                 mode=3,4/5,6.
            ('v_geo_corr', ((9, 17), float)),
            # 16 - V_geo_cor* (F8.1)  [m/s]   Velocity (word 15) after WATSCOR
            #                 correction*
            ('orbit', ((17, 23), int)),
            # 17 - Orbit  (I6)        orbit number
            ('altitude', ((23, 30), float)),
            # 18 - Altitude   (F7.1)  [km]
            ('lat', ((30, 36), float)),
            # 19 - Latitude   (F6.1)  [degree]  geographic latitude
            ('lon', ((36, 43), float)),
            # 20 - Longitude  (F7.1)  [degree]  geographic latitude
            ('lst', ((43, 49), float)),
            # 21 - LST    (F6.2)  [hours]   Local Solar Time
            ('lmt', ((49, 55), float)),
            # 22 - LMT    (F6.2)  [hours]   Local Magnetic Time
            ('l', ((55, 60), float)),
            # 23 - L      (F5.2)        McIllwain L value
            ('inv_lat', ((60, 66), float)),
            # 24 - Inv. Lat.  (F6.1)  [degree]  Invariant latitude
            ('sza', ((66, 73), float)),
            # 25 - SZA    (F7.1)  [degree]  Solar Zenith Angle
        ])
    ]
    drop_lines: int = 0
