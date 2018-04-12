# NACS
 NACS data is consist of 4644 data files and 1111894 datapoints. Among them:
 1. 558 files' UT data is not montonically increasing;
 2. 476 of 558 files contains duplicated UT values at the bottom of file;
 > This UT duplicates can be savely removed. It is not clear which of them is parasite, so we can drop both, those loosing 557 valid datapoints. Rate of lost is approximately 0.0062%.
 3. 94 of 558 files have UT jumps which are proved to be data after 12 AM, since UT data is measured in the boundaries of the day;
> Can be fixed by simply shifting all UT values since start of the jump on 86,400,000 milliseconds (1 day of milliseconds).

```
key: NACS
  Totals:
  8986459: total data points
    1111894: total data points in bad files
    12.37%: % of all datapoints in bad files
    1031168: total good datapoints in BAD files
    8905733: total good datapoints in ALL files
    99.1%: ratio of good datapoints to all datapoints
  4644: total data files
  558: total bad files
    94: midnight cut
      1 jumps in 94 files
    476: doppelgangers
      476: of them in the end of file
      0: of them NOT in the end of file
  0.005297%: rate of losts with removing doppledangers
```
List of all bad files at `README.NACS.BADFILES.txt`

# WATS
```
key: WATS
  Totals:
  3049552: total data points
    573038: total data points in bad files
    18.79%: % data points in bad files
    276053: total good datapoints in BAD files
    2752567: total good datapoints in ALL files
    90.26%: ratio of good datapoints to all datapoints
  534: total data files
  86: total bad files
    81: midnight cut
      1 jumps in 64 files
      2 jumps in 16 files
      3 jumps in 1 files
    7: doppelgangers
      0: of them in the end of file
      7: of them NOT in the end of file
  0.0002295%: rate of losts with removing doppledangers
```
List of all bad files at `README.WATS.BADFILES.txt`
