#!/usr/bin/python
import requests
from prettytable import PrettyTable

# DEFINE VARIABLES
controller_ip = '10.20.12.130' # UNCOMMENT AND EDIT THIS
target_api = 'wm/core/controller/switches/json' # UNCOMMENT AND EDIT THIS
headers = {'Content-type': 'application/json','Accept': 'application/json'}
url = f'http://{controller_ip}:8080/{target_api}'
response = requests.get(url=url, headers=headers)

if response.status_code == 200:
    # SUCCESSFUL REQUEST
    print('SUCCESSFUL REQUEST | STATUS: 200')
    data = response.json()
    table = PrettyTable(data[0].keys())
    for row in data:
        table.add_row(row.values())
    print(table)
else:
    # FAILED REQUEST
    print(f'FAILED REQUEST | STATUS: 200 {response.status_code}')

# FOR QUESTION 1h
# COMPLETE FOR PRINT ALL FLOWS PER SWITCH PID
# FIRST YOU NEED TO ASK USER INPUT A SWITCH PID
# AFTERWARD, BY USING THIS SWITCH PID, YOU SHOULD ASK THE PERTINENT API FOR GET ALL FLOWS PER SWITCH PID AND PRINT THEM (AS ABOVE CODE)
switch_DPID = input('Ingrese el DPID de un switch> ')
target_api = f'wm/core/switch/{switch_DPID}/flow/json' 
url = f'http://{controller_ip}:8080/{target_api}'
response = requests.get(url=url, headers=headers)

if response.status_code == 200:
    # SUCCESSFUL REQUEST
    print('SUCCESSFUL REQUEST | STATUS: 200')
    data = response.json()
    table = PrettyTable(data["flows"][0].keys())
    for row in data["flows"]:
        table.add_row(row.values())
    print(table)
else:
    # FAILED REQUEST
    print(f'FAILED REQUEST | STATUS: 200 {response.status_code}')
