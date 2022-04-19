from foam import Foam


# core
foam = Foam.from_file('tutorials/multiphase/compressibleMultiphaseInterFoam/laminar/damBreak4phase.yaml')
foam.save('damBreak4phase')
# info
# targets = ('fvSchemes', 'divSchemes', 'div(rhoPhi, U)')
# print(foam.info.search(*targets))
# print(set(foam.info.search_yaml(*targets)))
# cmd
codes = foam.cmd.all_run()
assert all(code==0 for code in codes)
# vtks
for time, vtk in zip(foam.cmd.times, foam.vtks):
    print(time, vtk.centroid('p'))
