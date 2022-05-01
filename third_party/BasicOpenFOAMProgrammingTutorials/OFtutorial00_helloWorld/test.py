from foam import Foam


foam = Foam \
    .from_file('testCase.yaml') \
    .save('testCase')
codes = foam.cmd.all_run()

assert all(code == 0 for code in codes)
