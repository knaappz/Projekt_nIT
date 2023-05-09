import argparse
import json
import yaml
import xmltodict
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description='Konwersja plików XML, JSON i YAML.')
parser.add_argument('input_file', type=str, help='Nazwa pliku wejściowego.')
parser.add_argument('output_file', type=str, help='Nazwa pliku wyjściowego.')
parser.add_argument('format', type=str, help='Format pliku')
args = parser.parse_args()

if args.input_file.endwith('.json'):
    with open(args.input_file, 'r') as j:
        try:
            data = json.load(j)
        except json.JSONDecodeError as e:
            print('Niepoprawnny format pliku...')
            exit(1)

elif args.input_file.endswith('.yaml'):
    with open(args.input_file, 'r') as y:
        try:
            data = yaml.safe_load(y)
        except yaml.YAMLError as e:
            print('Niepoprawny format pliku...')
            exit(1)

elif args.input_file.endswith('.xml'):
    tree = ET.parse(args.input_file)
    root = tree.getroot()
    data = xmltodict.parse(ET.tostring(root))

#funkcje  zapisujace nowy plik
if args.format == 'json':
    with open(args.output_file, 'w') as j:
        json.dump(data, j)

elif args.format == 'yaml' or 'yml':
    with open(args.output_file, 'w') as y:
        yaml.dump(data, y ,default_flow_style=False)

elif args.format == 'xml':
    xml_data = xmltodict.unparse(data, pretty=True)
    with open(args.output_file, 'w') as x:
        x.write(xml_data)
