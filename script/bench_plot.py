'''
{
    "extra/tutorial/tutorials/7/combustion/XiEngineFoam/kivaTest.yaml": [
        [6.067416335456073, 6.059840555302799],
        [6.1161600118502975, 6.008307630196214],
        [5.987000908702612, 6.0543485432863235],
        [6.09351275768131, 6.01447874493897],
        [6.02929066028446, 6.012912446632981],
        [6.1631866386160254, 6.035926444455981],
        [5.987829647958279, 6.058706551790237]
    ]
}
'''
from foam import Conversion
from foam.util.private.figure import Figure


data = Conversion.fromPath('bench.json').to_document()
times = []
for key, value in data.items():
    t1, t2 = map(list, zip(*value))
    times.append(sum(t1)/len(t1) - sum(t2)/len(t2))

Figure \
    .setRcParams(('axes.unicode_minus', False)) \
    .new(figsize=(8, 6)) \
    .mpl.hist(times) \
    .mpl.set(xlabel='Time (seconds)', title='$t_{shell}-t_{python}$') \
    .mpl.grid() \
    .save('demo.png')
