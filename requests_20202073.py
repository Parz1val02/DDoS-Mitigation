#!/usr/bin/python
#codigo: 20202073
import requests
from prettytable import PrettyTable

controller_ip = '10.20.12.130' # UNCOMMENT AND EDIT THIS
def get_attachment_points(mac,data):
    for row in data:
        if mac in row.get('mac', []):
            a_p = row.get('attachmentPoint',[])[0]
            s_dpid = a_p.get('switchDPID')
            port = a_p.get('port')
            break
    return s_dpid, port

def get_route(dpid_origen, port_origen, dpid_destino, port_destino):
    global controller_ip
    route_api = f'wm/topology/route/{dpid_origen}/{port_origen}/{dpid_destino}/{port_destino}/json'
    url = f'http://{controller_ip}:8080/{route_api}' 
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        print('SUCCESSFUL REQUEST | STATUS: 200')
        data = response.json()
        return data
    else:
        print(f'FAILED REQUEST | STATUS: {response.status_code}')
        return None




if __name__ == '__main__':
    #Identifique el método para encontrar el punto de conexión de un host, compuesto
    #por el DPID y el puerto del switch
    #http://10.20.12.130:8080/wm/device/

    # DEFINE VARIABLES
    target_api = 'wm/device/' # UNCOMMENT AND EDIT THIS
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
        mac_origen = input("Indicar MAC de host origen para obtener punto de conexión> ")
        switch_dpid_origen,port_origen=get_attachment_points(mac_origen, data)
        if switch_dpid_origen is not None and port_origen is not None:
            print(f'Para la mac origen:{mac_origen}\nswitchDPID:{switch_dpid_origen}\nport:{port_origen}')

        mac_destino = input("Indicar MAC de host destino para obtener punto de conexión> ")
        switch_dpid_destino,port_destino=get_attachment_points(mac_destino, data)
        if switch_dpid_destino is not None and port_destino is not None:
            print(f'Para la mac destino:{mac_destino}\nswitchDPID:{switch_dpid_destino}\nport:{port_destino}')
        
        data = get_route(switch_dpid_origen,port_origen,switch_dpid_destino, port_destino)
        if data is not None:
            table = PrettyTable(data[0].keys())
            for row in data:
                table.add_row(row.values())
            print(table)
    else:
        # FAILED REQUEST
        print(f'FAILED REQUEST | STATUS: {response.status_code}')