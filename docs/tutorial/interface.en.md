## Demo

Let's run the demo code in [IPython](https://github.com/ipython/ipython) (IPython is not included in the dependencies of the virtual environment) and after typing line by line we will get the following results. As you can see, the case runs perfectly fine and gives the estimated progress bar (thanks to [tqdm](https://github.com/tqdm/tqdm)).

```python
In [1]: from foam import Foam

In [2]: foam = Foam.from_file('tutorials/incompressible/simpleFoam/airFoil2D.yaml')

In [3]: foam.meta
Out[3]:
{'openfoam': [7],
 'version': '0.7.0',
 'order': ['meta', 'foam', 'static', 'other']}

In [4]: foam['foam']['system', 'controlDict', 'endTime'] = 365

In [5]: foam['foam']['system', 'controlDict']
Out[5]:
{'FoamFile': {'version': 2.0,
  'format': 'ascii',
  'class': 'dictionary',
  'object': 'controlDict'},
 'application': 'simpleFoam',
 'startFrom': 'startTime',
 'startTime': 0,
 'stopAt': 'endTime',
 'endTime': 365,
 'deltaT': 1,
 'writeControl': 'timeStep',
 'writeInterval': 50,
 'purgeWrite': 0,
 'writeFormat': 'ascii',
 'writePrecision': 6,
 'writeCompression': False,
 'timeFormat': 'general',
 'timePrecision': 6,
 'runTimeModifiable': True}

In [6]: foam.save('airFoil2D')
Out[6]: <Foam @ ".../tutorials/incompressible/simpleFoam">

In [7]: foam.cmd.all_run()
Running simpleFoam on .../airFoil2D
 86%|████████████████████████████████████████████████████▎        | 313.0/365.0 [00:06<00:01, 50.01it/s]
```



## Todo...

Perhaps next in this tutorial we can talk about the architecture of the interface library, the features that are expected to be added in the future, etc.
