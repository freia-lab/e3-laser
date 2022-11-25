# This should be a test or example startup script

require laser

iocshLoad("$(laser_DIR)/laser.iocsh", "LASER_IP=http://10.1.251.2:20010, OPA_IP=http://10.1.11.11:8004, EPP_IP=http://10.1.11.11:14001, P=Llab-, SCAN='2 second'")

epicsEnvShow PYTHONPATH

pydev("laser.debug=0")

pydev("opa.debug=0")
