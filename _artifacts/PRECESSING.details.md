# NACS
## Bad files
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

## Duplicates and intersections
```
key: NACS
  4086: total number of good datafiles

  a54a65cce790505e72e48a0341670e4ae48a89e1a02813a28ec1299c24f512fb
    1981267T231820_0_DE2_NACS_1S_V01.ASC
    1981267T231820_1_DE2_NACS_1S_V01.ASC

  de077d1c22a3a31ea5db6e7f2cd671f32f2e3c1f19cd2730fe01e3dcbd3cdbfa
    1981264T073640_0_DE2_NACS_1S_V01.ASC
    1981264T073640_1_DE2_NACS_1S_V01.ASC
  4084: total number of exclusive datafiles
  0 iteration. Intersection search
    24 files are intersecting
  1 iteration. Intersection search
    0 files are intersecting
4060 files left after filtering
7793701 datapoints left
```

# WATS
## Bad files
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

## Duplicates and intersections
```
key: WATS
  448: total number of good datafiles
  448: total number of exclusive datafiles
  0 iteration. Intersection search
    0 files are intersecting
448 files left after filtering
2476514 datapoints left

Duplicated files:

Intersected files:
```
