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

if args.format == 'json':
    with open(args.output_file, 'w') as j:
        json.dump(data, j)
