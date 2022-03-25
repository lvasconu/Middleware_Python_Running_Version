#!/bin/bash
# CR must be removed from this file!

# To start on boot Ref: https://www.tomshardware.com/how-to/run-script-at-boot-raspberry-pi:
# Make this file executable: mouse 2 > Properties > Permissions > Execute > Only owner.
# Create file:
#	sudo nano /etc/xdg/autostart/start_up_Middleware_rpi.desktop
# Put into it:
#	[Desktop Entry]
#	Exec=lxterminal --command="/bin/bash -c '/home/pi/Desktop/Middleware/start_up/start_up_Middleware_rpi.sh; /bin/bash'"

# Counting down.
for i in {5..1}
do
 echo "Starting Global Access Middleware in $i seconds"
 sleep 1
done

# Navigating to folder (apparentelly, absolute path is necessary for it to run on start up).
cd /home/pi/Desktop/Middleware

# Activating virtual environment.
echo Virtual environment - Activating.
source env/bin/activate
echo Virtual environment - Activated.

# Executing python 3 script:
python3 main.py