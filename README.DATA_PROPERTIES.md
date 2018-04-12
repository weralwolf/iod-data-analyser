# NACS
 NACS data is consist of 4644 data files and 8986459 datapoints. Among them:
 1. 557 files' UT data is not montonically increasing;
 2. 476 of 557 files contains duplicated UT values at the bottom of file;
 > This UT duplicates can be savely removed. It is not clear which of them is parasite, so we can drop both, those loosing 557 valid datapoints. Rate of lost is approximately 0.0062%.
 3. 94 of 557 files have UT jumps which are proved to be data after 12 AM, since UT data is measured in the boundaries of the day;
> Can be fixed by simply shifting all UT values since start of the jump on 86,400,000 milliseconds (1 day of milliseconds).
