# This should be a test or example startup script

require laser

iocshLoad("$(laser_DIR)/laser.iocsh", "LASER_IP=10.1.251.2,P=Llab-")

epicsEnvShow PYTHONPATH

