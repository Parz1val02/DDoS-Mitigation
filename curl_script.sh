#!/bin/bash                                                                                                                             │

# Set the interval between each curl command (in seconds)                                                                               │
target_url="http://10.0.0.21:3000"                                                                                                      │

# Set the interval between each curl command (in seconds)                                                                               │
interval=0.1                                                                                                                            │

while true; do                                                                                                                          │
    # Execute the curl command                                                                                                          │
    curl -I $target_url                                                                                                                 │

    # Sleep for the specified interval                                                                                                  │
    sleep $interval                                                                                                                     │
done  