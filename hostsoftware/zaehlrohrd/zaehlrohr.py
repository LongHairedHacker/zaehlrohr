#!/bin/env python2
import sys
import time
import signal

sys.path.append('../common/psql')

from dbmanager import DBManager
from sss7 import SSS7

from config import *

sss7_started = False

def signal_handler(signal, frame):
        if sss7_started:
            SSS7.stop()

        sys.exit(0)



def make_distance_matrix(distances):
    matrix = {}
    for a, b, distance in distances:
        if not a in matrix:
            matrix[a] = {}
        if not b in matrix:
            matrix[b] = {}

        matrix[a][b] = distance
        matrix[b][a] = distance

    return matrix



def main():
    global sss7_started

    signal.signal(signal.SIGINT, signal_handler)

    distances = make_distance_matrix(NODE_DISTANCES)

    dbman = DBManager(CONNECTION_STRING, EVENT_NAME)

    if not SSS7.start(SERIAL_DEVICE):
        print "Could not start sss7"
        sys.exit(-1)

    sss7_started = True

    last_node_id = None
    last_node_time = None


    MSG_ID = 0
    MSG_SRC = 1
    MSG_DST = 2

    MSG_TYPE_DETECTED = 0x00
    MSG_TYPE_START = 0x06


    while True:
        while not SSS7.has_received():
            time.sleep(0.100)

        msg = SSS7.get_received()

        if msg[MSG_ID] == MSG_TYPE_START:
            last_node_id = msg[MSG_DST]
            last_node_time = time.time()

        elif msg[MSG_ID] == MSG_TYPE_DETECTED:
            if last_node_id == None:
                current_node_id = msg[MSG_SRC]
                delta_time = time.time() - last_node_time

                event = {
                    'origin' : NODE_NAMES[last_node_id],
                    'destination': NODE_NAMES[current_node_id],
                    'velocity' : distances[last_node_id][current_node_id] / delta_time
                }

                dbman.insert_event(event)

            last_node_id = msg[MSG_SRC]
            last_node_time = time.time()



if __name__ == '__main__':
    main()
