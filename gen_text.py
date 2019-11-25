'''
Generate test.txt for testing manage_file_size.py
Note: Use timestamps to determine oldest data removed from file.
'''

import os
import datetime

line='{} 123456789012345678901234567890'.format(datetime.datetime.utcnow())
echo_cmd = 'echo {} > test.txt'.format(line)
os.system(echo_cmd)

for i in range(10000):
    line='{} 123456789012345678901234567890'.format(datetime.datetime.utcnow())
    echo_cmd = 'echo {} >> test.txt'.format(line)
    os.system(echo_cmd)
