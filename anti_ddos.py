import requests
import json
import subprocess
import time
from collections import defaultdict
from datetime import datetime

ip_to_switch_map = {}
controller_ip = "localhost"
controller_port = "8080"
controller_url = f"http://{controller_ip}:{controller_port}"

# Threshold for the number of requests per second
threshold = 5  # Adjust this based on your requirements
# Dictionary to store counts for each (source IP, destination IP) pair
request_counts = defaultdict(int)
current_second = None

def process_sflow_data(line):
    global threshold, request_counts, current_second, controller_url
    flow_entry_name = "drop_traffic_from_host"
    static_flow_pusher= 'wm/staticflowpusher/json'
    api = f"{controller_url}/{static_flow_pusher}"
    try:
        arch = False
        # Parse the sFlow data
        timestamp_str, agent_ip, src_ip, dst_ip = map(str.strip, line.split(','))
        # Parse the timestamp string
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S%z")
        # Extract the seconds
        seconds = timestamp.second
        #print(f"Timestamp: {timestamp_str}")
        #print(f"Seconds: {seconds}")
        # Calculate requests per second for each (source IP, destination IP) pair
        if current_second is None:
            current_second = seconds
        if current_second == seconds:
            key = (src_ip, dst_ip)
            key_inverse = (dst_ip, src_ip)
            if key_inverse in request_counts:
                request_counts[key_inverse] += 1
            else:
                request_counts[key] += 1
            # Check if the threshold is surpassed
            if (request_counts.get(key) is not None and request_counts.get(key)> threshold) or (request_counts.get(key_inverse) is not None and request_counts.get(key_inverse) > threshold):
                # Command to run
                curl_command = [
                'curl',
                '-X', 'DELETE',
                '-d', '{"name":"drop_traffic_from_host"}',
                'http://localhost:8080/wm/staticflowpusher/json'
                ]
                try:
                    # Run the curl command
                    subprocess.run(curl_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print(f"Threshold surpassed for {key}! DDoS detected!! Inserting flow entry in {agent_ip}...")
                    switch_dpid = get_switch_id_for_ip(agent_ip)
                    flow_entry = {
                    "switch": switch_dpid,
                    "name": flow_entry_name,
                    "cookie": "0",
                    "priority": "32768",
                    "eth_type": "0x0800",  # IPv4
                    "ipv4_src": src_ip,
                    "idle_timeout": "15",
                    "active": "true",
                    "actions": "drop"  
                    }
                    response = requests.post(api, data=json.dumps(flow_entry))
                    if response.status_code == 200:
                        print("Flow entry inserted successfully.")
                        # Reset the count after taking action
                        request_counts[key] = 0
                    else:
                        print("Error inserting flow entry. Status code:", response.status_code)
                        print("Response content:", response.content)
                    # Call your function to insert a flow entry here
                    # insert_flow_entry(agent_ip, src_ip, dst_ip)
                except subprocess.CalledProcessError as e:
                    print(f"Error executing command. Return code: {e.returncode}, Output: {e.output.decode()}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
        else:
            current_second = seconds
            request_counts.clear()
    except ValueError as e:
        print(f"Error processing line: {e}")


# Function to update the global dictionary
def update_ip_to_switch_mapping():
    global ip_to_switch_map, controller_url
    sw_dpid_ip= 'wm/core/controller/switches/json' 
    api = f"{controller_url}/{sw_dpid_ip}"
    headers = {'Content-type': 'application/json','Accept': 'application/json'}
    response = requests.get(url=api, headers=headers)
    if response.status_code == 200:
        print('SUCCESSFUL REQUEST | STATUS: 200')
        json_data = response.json()
        # Iterate through each item in the list
        for item in json_data:
            # Access values using keys
            inet_address = item['inetAddress']
            connected_since = item['connectedSince']
            switch_dpid = item['switchDPID']
            print(f"InetAddress: {inet_address}, Connected Since: {connected_since}, Switch DPID: {switch_dpid}")
            ip_address = inet_address.split('/')[1].split(':')[0]
            ip_to_switch_map[ip_address] = switch_dpid
    else:
        print(f"Error: {response.status_code}")

# Function to retrieve switch ID for a given IP address
def get_switch_id_for_ip(ip_address):
    global ip_to_switch_map
    return ip_to_switch_map.get(ip_address, None)

if __name__ == '__main__':
    update_ip_to_switch_mapping()
    ip_address_to_lookup = "192.168.200.201"
    switch_id = get_switch_id_for_ip(ip_address_to_lookup)
    if switch_id is not None:
        #print(f"Switch ID for IP {ip_address_to_lookup}: {switch_id}")
        # Command to run sflowtool with your desired arguments
        command = ["sflowtool", "-p", "6343", "-L", "localtime,agent,srcIP,dstIP"]
        #while True:
        try:
            # Run the command and capture the output stream
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                # Process the streaming output
            for line in iter(process.stdout.readline, ''):
                # Process each line as it becomes available
                #print(line, end='')
                process_sflow_data(line)
            # Wait for the process to complete
            process.wait()
                # Check for errors
            if process.returncode != 0:
                print(f"Error: {process.stderr.read()}")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"No switch ID found for IP {ip_address_to_lookup}")