__author__ = 'masslab'

from nist_config import *
import os

# Name and software version
software_name = "MEASURE 0.2"

# Database login
db_usr = nist_db_usr
db_pwd = nist_db_pwd
db_host_server = nist_db_host_server
db_schema = nist_db_schema

# This identifies the mass code path
masscode_path = nist_masscode_path

# This identifies the path of output files
output_path = r'L:\internal\684.07\Mass_Project\Customers\Calibration Reports'

# This identifies the location of the package folder MEASURE
package_path = os.path.abspath(os.path.dirname(__file__))

# This identifies the base path the program will use to when prompting the
# user for input file directory
base_path = nist_base_path

# Good balance response strings
good_responses = ['OK\r\n',
                  '\x11ready\r\n',
                  '\x13XON/XOFF handshake is enabled. \x11ready\r\n',
                  '\x13\x11ready\r\n']
# Bad response strings
error_responses = ['ES\r\n', ]

sleep_time = 0.2
long_command_timeout = 60
short_command_timeout = 10

max_timeouts = 3

# ---------------------Commands and statuses for balances control---------
AT106H = {'move': [['MOVE 1\r\n', 'MOVE 2\r\n', 'MOVE 3\r\n', 'MOVE 4\r\n'], ['Moving to position %s...', 'Movement complete', 'Error: failed to move to position %s']],
          'sink': [['SINK\r\n'], ['Sinking handler', 'Sink complete', 'Error: failed to sink handler']],
          'lift': [['LIFT\r\n'], ['Lifting handler', 'Lift complete', 'Error: failed to lift handler']],
          'beep': [['DB 1\r\n'], ['Beeping', 'Beep complete', 'Error: failed to beep']],
          'identify':   [['ID\r\n'], ['Identifying comparator', 'Id response:\n%s', 'Error: No balance response']],
          'resolution': [['RG F\r\n', 'RG C\r\n'], ['Setting balance resolution', 'Resolution set', 'Error: failed to set resolution%s']],
          'handshake on': [['HANDSHAKE_ON\r\n'], ['Turning handshake on', 'Handshake on', 'Error: failed to turn handshake on']],
          'open door': [['WI 0\r\n'], ['Opening door', 'Door open', 'Error: failed to open door']],
          'close door': [['WI 1\r\n'], ['Closing door', 'Door closed', 'Error: failed to close door']],
          'read': [['SI\r\n'], ['Integrating: %s s', 'Value: %s', 'Error: failed to read value']],
          'stab time':  'Stabilizing: %s s',
          'wait time': 'Executing wait time:\n%s left',
          'id': 68}

AX1006 = {'move': [['MOVE 1\r\n', 'MOVE 2\r\n', 'MOVE 3\r\n', 'MOVE 4\r\n'], ['Moving to position %s...', 'Movement complete', 'Error: failed to move to position %s']],
          'sink': [['SINK\r\n'], ['Sinking handler', 'Sink complete', 'Error: failed to sink handler']],
          'lift': [['LIFT\r\n'], ['Lifting handler', 'Lift complete', 'Error: failed to lift handler']],
          'beep': [['DB 1\r\n'], ['Beeping', 'Beep complete', 'Error: failed to beep']],
          'set unit': [['M21 0 3\r\n'], ['Setting unit to mg', 'Set to mg', 'Error']],
          'identify':   [['ID\r\n'], ['Identifying comparator', 'Id response:\n%s', 'Error: No balance response']],
          'resolution': [['RG F\r\n', 'RG C\r\n'], ['Setting balance resolution', 'Resolution set', 'Error: failed to set resolution%s']],
          'handshake on': [['HANDSHAKE_ON\r\n'], ['Turning handshake on', 'Handshake on', 'Error: failed to turn handshake on']],
          'open door': [['WI 0\r\n'], ['Opening door', 'Door open', 'Error: failed to open door']],
          'close door': [['WI 1\r\n'], ['Closing door', 'Door closed', 'Error: failed to close door']],
          'read': [['SI\r\n'], ['Integrating: %s s', 'Value: %s', 'Error: failed to read value']],
          'stab time':  'Stabilizing: %s s',
          'wait time': 'Executing wait time:\n%s left',
          'id': 69}

AX_MX_UMX = {'identify': [['I10\r\n'], ['Id response: %s']],
             'inquiry': [['I11\r\n'], ['Model: %s']],
             'open door': [['WI 0\r\n'], ['Opening door', 'Got reading: %s. Press Continue.', 'Error: failed to open door']],
             'close door': [['WI 1\r\n'], ['Closing door', 'Door closed', 'Error: failed to close door']],
             'read': [['S\r\n'], ['S S %s ']],
             'id': 70}

AT_MT_UMT = {'identify': [['ID\r\n'], ['Id response: %s']],
             'beep': [['DB 1\r\n'], ['beep']],
             'read': [['S\r\n'], ['Got measurement: %s Press continue.']],
             'tare': [['T\r\n'], ['Tare']],
             'open door': [['WI 0\r\n'], ['Opening door', 'Got reading: %s. Press Continue.', 'Error: failed to open door']],
             'close door': [['WI 1\r\n'], ['Closing door', 'Door closed', 'Error: failed to close door']],
             'stab time':  'Stabilizing: %s s',
             'id': 99}

Sartorius = {'identify': [['I10\r\n'], ['Id response: %s']],
             'read': [['S\r\n'], ['Got measurement: %s Press continue.']],
             'open door': [['WS 4\r\n'], ['Opening door', 'Got reading: %s. Press Continue.', 'Error']],
             'close door': [['WS 0\r\n'], ['Closing door', 'Door closed', 'Error']],
             'calibrate': [['C1\r\n'], ['%s']],
             'zero': [['Z\r\n'], ['%s']]}

# -----------------------------------------------------------------------------------
# This dictionary matches the balance to the set of commands it takes in

comparator_matching = {51: AX_MX_UMX,
                       53: AX_MX_UMX,
                       57: AX_MX_UMX,
                       59: AT_MT_UMT,
                       66: AX_MX_UMX,
                       68: AT106H,
                       69: AX1006,
                       70: AX_MX_UMX,
                       71: AX_MX_UMX,
                       72: AX_MX_UMX,
                       99: AT_MT_UMT,
                       41: AT_MT_UMT,
                       80: Sartorius}


