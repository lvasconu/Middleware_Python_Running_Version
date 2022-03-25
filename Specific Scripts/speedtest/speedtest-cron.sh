# Runnging python script and saving information on csv file.

# To create cron job (to run periodically): crontab -e
# Type the following line in the editor and save and exit by pressing Ctrl+X, Y, Enter:
# Minutes 00 and 30: 0,30 * * * * /home/pi/Desktop/speedtest/speedtest-cron.sh
# Minutes 15 and 45: 15,45 * * * * /home/pi/Desktop/speedtest/speedtest-cron.sh
# Ref: https://crontab.guru/

sudo python3 /home/pi/Desktop/speedtest/speedtest.py >> /home/pi/Desktop/speedtest/speedtest.csv
$SHELL