#!/bin/bash
echo "This scrip will install oled-sys.py as a service named oled-sys for the current user."
echo "The current user name is: $USER"

read -p "Do you want to proceed with installing this service? (y/n) " yn

case $yn in 
	y ) echo ok, we will proceed;;
	n ) echo exiting...;
		sleep 1
		exit;;
	* ) echo invalid response;
		sleep 1
		exit 1;;
esac

echo "Installing oled-sys.service to /etc/systemd/system/"
sleep .5
echo "[Unit]" | sudo tee /etc/systemd/system/oled-sys.service
echo "Description=OLED System Stats Service" | sudo tee -a /etc/systemd/system/oled-sys.service
echo "After=network.target" | sudo tee -a /etc/systemd/system/oled-sys.service
echo "StartLimitIntervalSec=0" | sudo tee -a /etc/systemd/system/oled-sys.service
echo "[Service]" | sudo tee -a /etc/systemd/system/oled-sys.service
echo "Type=simple" | sudo tee -a /etc/systemd/system/oled-sys.service
echo "Restart=always" | sudo tee -a /etc/systemd/system/oled-sys.service
echo "RestartSec=1" | sudo tee -a /etc/systemd/system/oled-sys.service
echo "User=$USER" | sudo tee -a /etc/systemd/system/oled-sys.service
echo "ExecStart=python3 /home/$USER/oled-sys/ft_sys.py" | sudo tee -a /etc/systemd/system/oled-sys.service
echo "[Install]" | sudo tee -a /etc/systemd/system/oled-sys.service
echo "WantedBy=multi-user.target" | sudo tee -a /etc/systemd/system/oled-sys.service
sleep .5
echo "Starting Service now..."
sudo systemctl start oled-sys
sleep .5
echo "Enabling Service now..." 
sudo systemctl enable oled-sys
sleep .5
echo "OLED-SYS SERVICE INSTALL COMPLETE!"
sleep 1
