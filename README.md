# Development
To bootstrap the project perform following commands:

For more details on instalation PROJ see http://proj4.org/install.html
```
pipenv install
```

## Project init
```
env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.6.5
```

# Prerequisits
pyenv, pipenv, autotool

### Installing cartography
For more details on instalation PROJ see http://proj4.org/install.html
```
pip install pyproj
mkdir builds && cd builds/
wget https://github.com/matplotlib/basemap/archive/v1.1.0.tar.gz
tar -xzvf v1.1.0.tar.gz
cd basemap-1.1.0/
cd geos-3.3.3/
export GEOS_DIR=/usr/local
./configure --prefix=$GEOS_DIR
make
make install
cd ..
python setup.py install
python -c "from mpl_toolkits.basemap import Basemap"
cd ..
cd ..
rm -rf builds
```

## Scripts
- `dev.bootstrap.project.sh` - bootstrap project;
- `dev.imports.sort.sh` - sorting imports in `requirements.txt`;
- `dev.lint.sh` - project linting against pep8;
- `dev.test.sh` - run project tests.

## Operations
1. `METHOD_spectr_analysis.m`
> Getting trends, spectras and other parameters (`O`, `N2`, `dz`, `vz`, `vy`, `T`, `P`);
2. `Proba_w_k_relation.m` (first 8 lines has value)
> - Looking for vector of local minimums of spectras. Usually require manual control.
> - Search for minimums located close from different spectras.

3. `CALCULATspectral_parameters.m`
> - Selecting spectral packages (scales) -> points of spectral packages on normalized disspersion plane.
> - Computing theoretical values and error boxes.
> - Computing energy, energy flow, internal environment energy, group/phase velocities (exp. vs. theor.).

4. `maximums.m`
> Working with spectral scales distinctively. Division on the packages in (`O`, `N2`) by synchrone behaviour of (`p`, `vz`, `vy`) in a couples. Create shape-curve over `O`, `N2` and uses Hilbert. Identify package spacial area via Hilbert's result for `O`.

5. `CALC_spectPar_Aria.m`
> Spectral parameters of each spacial package. Plot spectral parameters.

Valuable results:
  1. Point on disspersion plane;
  2. Direction of package propagation;

# Decissions
Studying data where's a handfull of questions we must ask ourselves on the way to understand boundaries of our thechniques applicability and attempts to get longest continious sequence of good data.

## Sampling
For application of scientific methods we must obtain equaly sampled lengthy data available in a number of channels. There's a few questions worth of descussing.
Lets say `S` is a sampling we are interested in.

### Break points identification
For different samplings we can take a few stategies of breakpoints identification:
1. Break data continuity on gaps longer than `\alpha S`, where `\alpha <= 1` is density parameter;
2. Select data with segments with equal sampling in original data;

This strategy can be made costumary.

### Best sampling identification
Having a continuous data best sampling frequency can be identified through variation of error-function and selecting local minimum. It is necessary to select responsible error function which will approximate and minimize resampling error.
```
error = \sqrt{\Sum^{|ch|}_a(ch(a) - ch'(a))^2}
```

### Boundaries of resempling applicability
Identify reasonable boundaries of methodology applicability according to different sampling strategies. Identify areas of best applicability.

## Conectivity
Identification of lengthy segments is crucial for sake of having good data for analysis.

### Overlaping data
Data cross-overs must be excluded from data consideration. Later selection  strategies can be introduced.

### Data filtering
Simplify filtering mechanisms to preproduce and clean up data before processing.

### Slicing methodologies
Models of storing identified structure and find areas of data intersection over different channels.

## Methodology verification
It is important to see precission of our methodology in identification of different fenomenas and get full connection between data generation and data measurement.

### Models of AGW sources
### Trend models
### PDE earth-like grids
### Satellite measurements emulation
### Methodology error function


# Troubleshooting
## Matplotlib
> RuntimeError: Python is not installed as a framework. The Mac OS X backend will not be able to function correctly if Python is not installed as a framework. See the Python documentation for more information on installing Python as a framework on Mac OS X. Please either reinstall Python as a framework, or try one of the other backends. If you are using (Ana)Conda please install python.app and replace the use of 'python' with 'pythonw'. See 'Working with Matplotlib on OSX' in the Matplotlib FAQ for more information.

```
env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.5.4
```

## Matplotlib basemap
If during drawing maps there's a strange exception... Take a look here: https://github.com/matplotlib/basemap/issues/197

`ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()` line 4783. Change statement to `if False:`.

Edit `<virtualend path>/lib/python3.6/site-packages/mpl_toolkits/basemap/__init__.py`


# Future plans
1. Time map with d3: http://bl.ocks.org/tnightingale/4718717

# Drowing dynamic maps
1. https://bl.ocks.org/mbostock/4481520
2. https://bl.ocks.org/mbostock/4458497
3. https://www.theguardian.com/environment/interactive/2013/may/14/alaska-villages-frontline-global-warming
4. https://www.toptal.com/javascript/a-map-to-perfection-using-d3-js-to-make-beautiful-web-maps
5. http://datamaps.github.io/
6. https://medium.com/@andybarefoot/making-a-map-using-d3-js-8aa3637304ee
7. https://bost.ocks.org/mike/map/
8. http://www.tnoda.com/blog/2013-12-07

# Diploma tasks
## До 2 квітня (02.04.2018)
### Код
1. Розпізнавання здвоєних за ut шматків, список ігнорування;
2. Розбиття за семплінгом;
3. Намалювати треки;
4. Визначити близькі;
### Документ
1. Вивчити Тетянину статтю;
2. Зробити оглядовий розділ;
## До 17 квітня (17.04.2018)
### Код
1. Ресемплінг даних;
2. Місця перекриття даних NACS та WATS;
### Документ
1. Описати методику;
2. Чорновик обробки даних;

Знайти своє місце в обробці. Зрозуміти, що я шукаю, що локалізовую.


# Interpolation of Irregularly Sampled Data Series
1. [Interpolation of Irregularly Sampled Data Series---A Survey](ftp://ftp.adass.org/adass/proceedings/adass94/adorfhm2.html)
2. [Resampling Nonuniformly Sampled Signals](https://www.mathworks.com/help/signal/examples/resampling-nonuniformly-sampled-signals.html)
3. [Unevenly spaced time series](https://www.wikiwand.com/en/Unevenly_spaced_time_series)
4. [How to Normalize and Standardize Time Series Data in Python](https://machinelearningmastery.com/normalize-standardize-time-series-data-python/)
5. [A gentle inroduction to resampling techniques](https://pdfs.semanticscholar.org/9cd6/be2808c9827bbaf8f479461bf730cee2d70a.pdf)
6. [How To Resample and Interpolate Your Time Series Data With Python](https://machinelearningmastery.com/resample-interpolate-time-series-data-python/)
7. [Fourier transforms of data sampled in unequally spaced segments](http://adsbit.harvard.edu/cgi-bin/nph-iarticle_query?1979AJ.....84..116M&defaultprint=YES&filetype=.pdf)
8. [Generalized nonlinear inverse problems solved using the least squares criterion](http://www.ipgp.fr/~tarantola/Files/Professional/Papers_PDF/GeneralizedNonlinear_original.pdf)
9. [Algorithms for Unevenly Spaced Time Series: Moving Averages and Other Rolling Operators](http://eckner.com/papers/Algorithms%20for%20Unevenly%20Spaced%20Time%20Series.pdf)
10. [Comparison of correlation analysis techniques for irregularly sampled time series](https://www.nonlin-processes-geophys.net/18/389/2011/npg-18-389-2011.pdf)
11. [A Framework for the Analysis of Unevenly Spaced Time Series Data](http://www.eckner.com/papers/unevenly_spaced_time_series_analysis.pdf)
12. [A Note on Trend and Seasonality Estimation for Unevenly Spaced Time Series](http://eckner.com/papers/Trend%20and%20Seasonality%20Estimation%20for%20Unevenly%20Spaced%20Time%20Series.pdf)
13. [Andreas Eckner research page. Unevenly spaced time series publications](http://www.eckner.com/research.html)
14. [Repeat in strings](http://www.cs.ucr.edu/~stelo/cpm/cpm14/00_Crochemore.pdf)
