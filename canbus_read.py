#!/usr/bin/env python
"""Extracts messages from CAN Bus interface and persists to Extract queue"""

import os

import can
from can import Message

pids = {
    # list of PID bytearrays to query
    "vehicle_speed": Message(
        arbitration_id=0x7DF,
        extended_id=False,
        data=[0x2, 0x1, 0xD, 0x55, 0x55, 0x55, 0x55, 0x55],
    ),
    "engine_load": Message(
        arbitration_id=0x7DF,
        extended_id=False,
        data=[0x2, 0x1, 0x4, 0x55, 0x55, 0x55, 0x55, 0x55],
    ),
    "coolant_temp": Message(
        arbitration_id=0x7DF,
        extended_id=False,
        data=[0x2, 0x1, 0x5, 0x55, 0x55, 0x55, 0x55, 0x55],
    ),
    "engine_rpm": Message(
        arbitration_id=0x7DF,
        extended_id=False,
        data=[0x2, 0x1, 0xC, 0x55, 0x55, 0x55, 0x55, 0x55],
    ),
    "throttle_position": Message(
        arbitration_id=0x7DF,
        extended_id=False,
        data=[0x2, 0x1, 0x11, 0x55, 0x55, 0x55, 0x55, 0x55],
    ),
    "ambient_air_temperature": Message(
        arbitration_id=0x7DF,
        extended_id=False,
        data=[0x2, 0x1, 0x46, 0x55, 0x55, 0x55, 0x55, 0x55],
    ),
}


def query_pids(bus, pids):
    """Send queries for all PIDs of interest"""
    for pid in pids:
        bus.send(pid)
    return



def send_req():
    while True:
        print("Sending message")
        bus.send(speed_req)
        time.sleep(2)


##### main loop

what to capture

# Measurement   PID (hex)      data bytes returned    Metric/calc
# engine load           4      1                      % (A/255)
# coolant temp          5      1                      Celcius (A-40)
# engine RPM            C      2                      rpm (256 x A + B)/4
# vehicle speed         D      1                      Km/h  A
# throttle position     11     1                      % (100/255)*A
# ambient air temp      46     1     

bus = can.Bus(interface="kvaser", channel=0, receive_own_messages=True)

msg_thread = threading.Thread(target=send_req)
msg_thread.start()

for msg in bus:
    if msg.arbitration_id == 0x7E8:
        print("0x{:02x}: {}".format(msg.arbitration_id, msg.data))
