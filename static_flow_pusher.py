import requests
import json

def insert_flow_entry_ssh(controller_url, dest_switch_dpid, flow_entry_name, action):
    flow_entry = {
    "switch": dest_switch_dpid,
    "name": flow_entry_name,
    "cookie": "0",
    "priority": "32768",
    "eth_type": "0x0800",  # IPv4
    "ip_proto": "6",  # 6 corresponds to TCP
    "tcp_dst": "22",  # Destination port 22 (SSH)
    "active": "true",
    "actions": action  
    }
    flow_entry_url = f"{controller_url}/wm/staticflowpusher/json"

    response = requests.post(flow_entry_url, data=json.dumps(flow_entry))
    if response.status_code == 200:
        print("Flow entry inserted successfully.")
    else:
        print("Error inserting flow entry. Status code:", response.status_code)
        print("Response content:", response.content)

def remove_flow_entry(controller_url, flow_entry_name):
    flow_entry_url = f"{controller_url}/wm/staticflowpusher/json"
    data = {
    "name": flow_entry_name
    }
    response = requests.delete(flow_entry_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print(f"Flow entry '{flow_entry_name}' removed successfully.")
    else:
        print(f"Error removing flow entry. Status code: {response.status_code}")
        print("Response content:", response.content)

if __name__ == '__main__':
    ip = "10.20.12.130"
    port = "8080"
    controller_url = f"http://{ip}:{port}"
    print("######################################")
    print("Flow entries")
    print("######################################")
    print("Seleccione una opción")
    print("a) Agregar flow entry")
    print("b) Quitar flow entry")
    accion = input("> ")
    match accion:
        case 'a':
            dest_switch_dpid = input("Ingrese el dpid del switch destino> ")
            print("Seleccione una opción")
            print("1) Permitir conexion ssh")
            print("2) Denegar conexion ssh")
            option = input("> ")
            match option:
                case '1':
                    flow_entry_name = input("Ingrese el nombre del flow entry a agregar> ")
                    dest_port= input("Ingrese el puerto del switch destino> ")
                    insert_flow_entry_ssh(controller_url, dest_switch_dpid, flow_entry_name, f'output={dest_port}')
                case '2':
                    flow_entry_name = input("Ingrese el nombre del flow entry a agregar> ")
                    insert_flow_entry_ssh(controller_url, dest_switch_dpid, flow_entry_name, 'drop')
                case _:
                    print("Error. Saliendo del programa")
        case 'b':
                flow_entry_name = input("Ingrese el nombre del flow entry a quitar> ")
                remove_flow_entry(controller_url, flow_entry_name)
        case _:
            print("Error. Saliendo del programa")