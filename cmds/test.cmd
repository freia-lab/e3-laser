# This should be a test or example startup script

require laser

pydev("import sys")
pydev("sys.path.append('$(laser_DIR)')")

pydev("from myTest import MyTest")
pydev("tst=MyTest(100)")
dbLoadRecords("test.db", "SCAN='.1 second'")

epicsEnvShow PYTHONPATH
