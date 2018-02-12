# Development
To bootstrap the project perform following commands:

```
virtualenv -p python3
source env/bin/activate
pip install -r requirements.txt
```

### `dev.bootstrap.project.sh`
Bootstrap project.

### `dev.imports.sort.sh`
### `dev.lint.sh`
### `dev.test.sh`
### `dev.venv.delete`
### `dev.venv.switch`

## Operations
1. METHOD_spectr_analysis.m
Getting trends, spectras and other parameters (O, N2, dz, vz, vy, T, P)

2. Proba_w_k_relation.m (First 8 lines has value)
Looking for vector of local minimums of spectras. Usually require manual control.
Search for minimums located close from different spectras.

3. CALCULATspectral_parameters.m
Selecting spectral packages (scales) -> points of spectral packages on normalized disspersion plane.
Computing theoretical values and error boxes.
Computing energy, energy flow, internal environment energy, group/phase velocities (exp. vs. theor.)

4. maximums.m
Working with spectral scales distinctively. Division on the packages in (O, N2) by synchrone behaviour of (p, vz, vy) in a couples. Create shape-curve over O, N2 and uses Hilbert. Identify package spacial area via Hilbert's result for O.

5. CALC_spectPar_Aria.m
Spectral parameters of each spacial package. Plot spectral parameters.

Valuable results:
	1. Point on disspersion plane;
	2. Direction of package propagation;


# Drowing dynamic maps
https://bl.ocks.org/mbostock/4481520
https://bl.ocks.org/mbostock/4458497
https://www.theguardian.com/environment/interactive/2013/may/14/alaska-villages-frontline-global-warming
https://www.toptal.com/javascript/a-map-to-perfection-using-d3-js-to-make-beautiful-web-maps
http://datamaps.github.io/
https://medium.com/@andybarefoot/making-a-map-using-d3-js-8aa3637304ee
https://bost.ocks.org/mike/map/
http://www.tnoda.com/blog/2013-12-07