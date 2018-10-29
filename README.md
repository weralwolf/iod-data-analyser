# Development
To bootstrap the project perform following commands:

For more details on installation PROJ see [http://proj4.org/install.html](http://proj4.org/install.html)  pipenv install

# Ipython autoreload
```
%load_ext autoreload
%autoreload 2
```

# Method
[https://github.com/Skorokhodik/IonosphereData.git](https://github.com/Skorokhodik/IonosphereData.git)

# Prerequisites
Docker

# Operations
- METHODspectranalysis.m
> Getting trends, spectra and other parameters (O, N2, dz, vz, vy, T, P);
- Probawk_relation.m (first 8 lines has value)
> - Looking for vector of local minimums of spectra. Usually require manual control.
  - Search for minimums located close from different spectra.

- CALCULATspectral_parameters.m
> - Selecting spectral packages (scales) -> points of spectral packages on normalised dispersion plane.
  - Computing theoretical values and error boxes.
  - Computing energy, energy flow, internal environment energy, group/phase velocities (exp. vs. theor.).

- maximums.m
> Working with spectral scales distinctively. Division on packages in (O, N2) by synchrony behaviour of (p, vz, vy) in a couples. Create shape-curve over O, N2 and uses Hilbert. Identify package spacial area via Hilbert's result for O.

- CALCspectParAria.m
> Spectral parameters of each spacial package. Plot spectral parameters.

Valuable results:
- Point on dispersion plane;
- Direction of the package propagation;

# Decisions
dying data where's a handful of questions we must ask ourselves on the way to understand boundaries of our techniques applicability and attempts to get longest continuous sequence of good data.

# Sampling
For application of scientific methods we must obtain equally sampled lengthy data available in a number of channels. There's a few questions worth of discussing.
Lets say S is a sampling we are interested in.

# Break points identification
For different samplings we can take a few strategies of breakpoints identification:
- Break data continuity on gaps longer than \alpha S, where \alpha <= 1 is density parameter;
- Select data with segments with equal sampling in original data;

This strategy can be made customary.

# Best sampling identification
Having a continuous data best sampling frequency can be identified through variation of error-function and selecting local minimum. It is necessary to select responsible error function which will approximate and minimise resampling error.  error = \sqrt{\Sum^{|ch|}_a(ch(a) - ch'(a))^2}


# Boundaries of resampling applicability
Identify reasonable boundaries of methodology applicability according to different sampling strategies. Identify areas of best applicability.

# Machine learning

# Trend extraction
Extract trend from a signal using neural-network. Create a samples using a few deterministic algorithms described at ISTS/12.

# Event selection
Create a dataset with selected wave-events and teach algorithm to detect them.

# Infrastructure
Docker infrastructure modularised as:
- data-analyser - Python code producing analysis artefacts;
- report-engine - TypeScript report generator from processing artefacts;
- paper-processor - LaTeX processor to process papers, presentations, notes;
- data-processor - C++ data processing backend, making python port for parsers and writers;

# Future plans
- Time map with d3: [http://bl.ocks.org/tnightingale/4718717](http://bl.ocks.org/tnightingale/4718717)

# [DDM] Drawing dynamic maps
- [https://bl.ocks.org/mbostock/4481520](https://bl.ocks.org/mbostock/4481520)
- [https://bl.ocks.org/mbostock/4458497](https://bl.ocks.org/mbostock/4458497)
- [https://www.theguardian.com/environment/interactive/2013/may/14/alaska-villages-frontline-global-warming](https://www.theguardian.com/environment/interactive/2013/may/14/alaska-villages-frontline-global-warming)
- [https://www.toptal.com/javascript/a-map-to-perfection-using-d3-js-to-make-beautiful-web-maps](https://www.toptal.com/javascript/a-map-to-perfection-using-d3-js-to-make-beautiful-web-maps)
- [http://datamaps.github.io/](http://datamaps.github.io/)
- [https://medium.com/@andybarefoot/making-a-map-using-d3-js-8aa3637304ee](https://medium.com/@andybarefoot/making-a-map-using-d3-js-8aa3637304ee)
- [https://bost.ocks.org/mike/map/](https://bost.ocks.org/mike/map/)
- [http://www.tnoda.com/blog/2013-12-07](http://www.tnoda.com/blog/2013-12-07)


# [ISTS] Interpolation of Irregularly Sampled Data Series
- [Interpolation of Irregularly Sampled Data Series---A Survey](ftp://ftp.adass.org/adass/proceedings/adass94/adorfhm2.html)
- [Resampling Nonuniformly Sampled Signals](https://www.mathworks.com/help/signal/examples/resampling-nonuniformly-sampled-signals.html)
- [Unevenly spaced time series](https://www.wikiwand.com/en/Unevenly_spaced_time_series)
- [How to Normalize and Standardize Time Series Data in Python](https://machinelearningmastery.com/normalize-standardize-time-series-data-python/)
- [A gentle inroduction to resampling techniques](https://pdfs.semanticscholar.org/9cd6/be2808c9827bbaf8f479461bf730cee2d70a.pdf)
- [How To Resample and Interpolate Your Time Series Data With Python](https://machinelearningmastery.com/resample-interpolate-time-series-data-python/)
- [Fourier transforms of data sampled in unequally spaced segments](http://adsbit.harvard.edu/cgi-bin/nph-iarticle_query?1979AJ.....84..116M&defaultprint=YES&filetype=.pdf)
- [Generalized nonlinear inverse problems solved using the least squares criterion](http://www.ipgp.fr/~tarantola/Files/Professional/Papers_PDF/GeneralizedNonlinear_original.pdf)
- [Algorithms for Unevenly Spaced Time Series: Moving Averages and Other Rolling Operators](http://eckner.com/papers/Algorithms%20for%20Unevenly%20Spaced%20Time%20Series.pdf)
- [Comparison of correlation analysis techniques for irregularly sampled time series](https://www.nonlin-processes-geophys.net/18/389/2011/npg-18-389-2011.pdf)
- [A Framework for the Analysis of Unevenly Spaced Time Series Data](http://www.eckner.com/papers/unevenly_spaced_time_series_analysis.pdf)
- [A Note on Trend and Seasonality Estimation for Unevenly Spaced Time Series](http://eckner.com/papers/Trend%20and%20Seasonality%20Estimation%20for%20Unevenly%20Spaced%20Time%20Series.pdf)
- [Andreas Eckner research page. Unevenly spaced time series publications](http://www.eckner.com/research.html)
- [Repeat in strings](http://www.cs.ucr.edu/~stelo/cpm/cpm14/00_Crochemore.pdf)
- [Statistical Learning: Algorithmic and Nonparametric Approaches](https://rafalab.github.io/pages/649/)
- [fminunc - Coursera ML minimisation function python impl.](https://stackoverflow.com/a/21952908/1367936)
