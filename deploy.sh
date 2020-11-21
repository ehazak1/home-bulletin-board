#!/bin/sh

# Give write permission to www-data


# Create check for internet connection
#sudo usermod -a -G www-data pi
#sudo chgrp www-data /home/pi/cfjc/
#sudo chmod g+rwxs /home/pi/cfjc/

echo "****** Updating and Raspbian repostories ******"
sudo apt-get update
if [ $? -ne 0 ];
    echo "ERROR: Failed updating repositories"
fi

echo "****** Installing Nginx and python3-pip ******"
sudo apt-get install -y nginx python3-pip
if [ $? -ne 0 ];
    echo "Error: Failed installing packages"
fi

echo "****** Cloning GIT Repository  ******"
cd ~
git clone https://github.com/ehazak1/home-bulletin-board.git
if [ $? -ne 0 ];
    echo "Error: Failed cloning "
fi

