#!/bin/env python2
import serial
import time
import sys

from config import Config
from statemachine import StateMachine
from states import *


ser = serial.Serial(Config.serialdevice, Config.baudrate, timeout=Config.timeout)
if not ser:
  print "Unable to open serial port"
  sys.exit(1)


statemachine = StateMachine(ser)
statemachine.register_state(ResetState())
statemachine.register_state(OutOfSyncState())
statemachine.register_state(RunningState(Config.json_log))
statemachine.switch_state("reset")

while True:
	statemachine.execute()

