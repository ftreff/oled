echo "This script will upgrade your existing packages and install the python3 luma.oled and psutil packages."
sleep 2
echo "*----Updating package lists----*"
sleep .5
yes | sudo apt update
echo "*----Upgrading packages----*"
sleep .5
yes | sudo apt upgrade
echo "*----Installing python3-luma.oled----*"
sleep .5
yes | sudo apt install python3-luma.oled
echo "*----Installing python3-psutil----*"
sleep .5
yes | sudo apt install python3-psutil
echo "*****  Complete!  *****"
sleep 2
