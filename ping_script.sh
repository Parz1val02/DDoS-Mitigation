#!/bin/bash                                                                                                                             │

#Replace 'TARGET_HOST' with the actual IP address or hostname you want to ping                                                          │
TARGET_HOST="10.0.0.21"                                                                                                                 │

# Sleep interval between each ping request (in seconds)                                                                                 │
SLEEP_INTERVAL=0.01                                                                                                                     │

# Loop to send ping requests                                                                                                            │
while true; do                                                                                                                          │
    ping -c 1 -i 0.2 $TARGET_HOST                                                                                                       │
    sleep $SLEEP_INTERVAL                                                                                                               │
done  