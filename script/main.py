from foam import Foam


# core
foam = Foam.from_file('tutorials/incompressible/simpleFoam/airFoil2D.yaml')
foam.save('airFoil2D')
# info
targets = ('fvSchemes', 'divSchemes', 'div(rhoPhi, U)')
print(foam.info.search(*targets))
print(set(foam.info.search_yaml(*targets)))
# cmd
codes = foam.cmd.all_run()
assert all(code==0 for code in codes)
# vtks
for time, vtk in zip(foam.cmd.times, foam.post.vtks):
    print(time, vtk.centroid('p'))
