# TnPcal

This project is meant to be a versatile, flexible and user friendly way to measure efficiencies using the Tag and Probe method.

## How does it work?

The logic of the method is that one would apply a requirement to a dataset and out of it, a certain number of samples would pass it.
The fraction of successes is called, the _efficiency_. E.g. one takes the population of a country and requires it to be male, 50%
of the population passes, the efficiency is 0.5.

However in HEP one needs to deal with datasets that are a mixture of different categories, for simplicity, we will call them signal
and background. We are only interested on the signal; thus, we need a way to remove the background when calculating the signal efficiency.
There are two ways to do this:

- sWeigths: Weights are calculated through the sPlot technique or other approach and the weighted dataset is assumed to be pure signal.o

- Fits: The distribution of interest (usually the mass of a particle) is fitted. Thus we can separate the signal yield and study it.

## Fitting approach

In order to extract a good (low uncertainty) signal yield from the fit, such that we can know the efficiency of a cut on it, we have to
make sure that the sample we start with is _clean enough_ and _unbiased_. By this we mean:

- clean enough: We can see a nice, large peak with little background.

- unbiased: The properties of this clean sample are the same as the ones for the original one. I.e. the cleaning process does not
change the efficiencies.

Thus a tagging requirement is needed. Once the tagging is done, we fit and extract the efficiencies.


# Usage

## Fitting approach

```python
from tnpcal.fitter import Fitter as TnPFitter

obj = TnPFitter(data=df, model=mod, cfg=cfg)
obj.run()
```

The code will take:

- A pandas dataframe with the data
- The fitting model, implemented with zfit
- The configuration through the `cfg` dictionary 

and run all the fits as well as calculate all the efficiencies. The configuration is as shown below:

```yaml
observable:
    name    : mass
    min_val : 5000
    max_val : 6000
selection:
    tag   : 'purity > 0.8' #Quantity that drives signal purity, e.g 1 means only signal 0 means full mix
    probe : 'quantity'     #Quantity, whose efficiency needs to be measured
```

