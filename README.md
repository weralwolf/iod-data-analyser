# Development
To bootstrap the project perform following commands:

```
virtualenv -p python3
source env/bin/activate
pip install -r requirements.txt
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

