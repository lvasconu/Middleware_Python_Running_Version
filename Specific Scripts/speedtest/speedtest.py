# Refs:
# Speedtest: https://thepi.io/how-to-use-your-raspberry-pi-to-monitor-broadband-speed/
# Cron: https://crontab.guru/every-15-minutes , https://www.hostinger.com.br/tutoriais/cron-job-guia/
# Test in windows: python speedtest.py > "C:\\Users\\joaoo\\Desktop\\speedtest.csv"

# Install speedtest-cli: sudo pip install speedtest-cli

import os
import re
import subprocess
import time

response = subprocess.Popen('speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read()

ping = re.findall('Ping:\s(.*?)\s', response.decode(), re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', response.decode(), re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', response.decode(), re.MULTILINE)

# Replacing , to .
ping[0]     = ping[0].replace(',', '.')
download[0] = download[0].replace(',', '.')
upload[0]   = upload[0].replace(',', '.')

try:
    if os.stat('/home/pi/Desktop/speedtest/speedtest.csv').st_size == 0:
    #if os.stat('C:\\Users\\joaoo\\Desktop\\speedtest.csv').st_size == 0:
        print('Date,Time,Ping (ms),Download (Mbit/s),Upload (Mbit/s)')
except:
    pass

print('{},{},{},{},{}'.format(time.strftime('%d/%m/%Y'), time.strftime('%H:%M'), ping[0], download[0], upload[0]))