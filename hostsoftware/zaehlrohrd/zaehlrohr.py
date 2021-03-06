#!/bin/env python2
import sys
import serial
import time

from config import Config
from statemachine import StateMachine
from states import *
from outputs import *


ser = serial.Serial(Config.serialdevice, Config.baudrate, timeout=Config.timeout)
if not ser:
  print "Unable to open serial port"
  sys.exit(1)


statemachine = StateMachine(ser)
statemachine.register_state(ResetState())
statemachine.register_state(OutOfSyncState())
statemachine.register_state(RunningState([PsqlOutput(), ]))
statemachine.switch_state("reset")

while True:
	statemachine.execute()

