#!/bin/bash

# Get user input/
echo "Name of wireless interface:"
read iface

# Check if there's an internet connection/
# Check google.com to test if it's reachable remotely/
# So "> /dev/null 2>&1" first redirects stdout to /dev/null and then redirects stderr there as well. This effectively
# silences all output (regular or error) from the 'ping' command/
ping -c 1 google.com > /dev/null 2>&1
exit_status=$? # Store the exit status of the ping command/

# Check if there's internet access/
if [[ $exit_status -eq 0 ]]
  then
    echo "Starting..."
  else
    echo "No internet connection! Try to turn on the Wi-Fi."
    exit 1;
fi
# Compute and process/
# Set the wireless interface, iface, down to enable 'macchanger' program operations/
sudo ip link set $iface down

# Randomly change the current MAC address with the macchanger program/
sudo macchanger --random $iface

# Set the wireless interface, iface, up again/
sudo ip link set $iface down

# output the feedback
