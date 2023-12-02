#!/usr/bin/python
#codigo: 20202073
import yaml

if __name__ == '__main__':
    file_path = './datos.yaml'
    with open(file_path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
        for key, inner_dict in data.items():
            if(key.lower() == 'servidores'):
                for data2 in inner_dict:
                    for key2, inner_dict2 in data2.items():
                        if(key2.lower() == 'nombre'):
                            print(inner_dict2)



