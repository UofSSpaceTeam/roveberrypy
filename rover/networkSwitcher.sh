#!/bin/bash

if [ "$(id -u)" != "0" ]
	then
	  echo "You should be root! Try running command with sudo."
	  exit 1
fi

if [ -e /etc/network/interfaces ]
        then
	  cp /etc/network/interfaces /etc/network/interfaces.old
	else echo "No network configuration file... exiting!  You might have to do it manually :("
fi

if [ -e /etc/network/interfaces.old ]
	then
	  echo "Backup complete."
	else echo "Failed.  Try running as admin."
	exit 1
fi

echo "Which Pi is this?"
select daem in "Drive" "Arm" "Experiment" "Mast" "Base; do
    case $daem in
        Drive )
	  echo "Raspi1 Selected: 192.168.1.103"
	  name=raspi1
	  address=192.168.1.103
	  break;;
        Arm )
	  echo "Raspi2 Selected: 192.168.1.104"
	  name=raspi2
	  address=192.168.1.104
	  break;;
	Experiment )
	  echo "Raspi3 Selected: 192.168.1.105"
	  name=raspi3
	  address=192.168.1.105
	  break;;
	Mast )
	  echo "Raspi4 Selected: 192.168.1.106"
	  name=raspi4
	  address=192.168.1.106
	  break;;
	Base )
	  echo "basepi Selected: 192.168.1.110"
	  name=basepi
	  address=192.168.1.110
	  break;;
    esac
done
    
echo "Ready to switch network modes on Pi.  900MHZ for Rover Comms, DHCP for LAN and Internet"
select ab in "900MHZ" "DHCP"; do
    case $ab in
        900MHZ )
          echo "Connecting to Rover network."
          echo "auto lo
iface lo inet loopback
iface eth0 inet static
	name ${name}
	address ${address}
	netmask  255.255.255.0
	gateway 192.168.1.102

allow-hotplug wlan0
iface wlan0 inet manual
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp" > /etc/network/interfaces
	
        break;;
        
        DHCP )
          echo "resetting to DHCP"
          echo "auto lo
iface lo inet loopback

auto eth0
allow-hotplug eth0
iface eth0 inet dhcp

allow-hotplug wlan0
iface wlan0 inet manual
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf

iface default inet dhcp" > /etc/network/interfaces
        
        break;; 
    esac
done

echo "Resetting network interfaces..."

/etc/init.d/networking stop && /etc/init.d/networking start

exit
