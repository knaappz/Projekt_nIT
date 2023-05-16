import argparse
import json
import yaml
import xml.etree.ElementTree as ET
import xmltodict
import xml.dom.minidom

# Tworzenie parsera argumentów
parser = argparse.ArgumentParser(description='Konwerter plików json, xml, yaml')
parser.add_argument('input_file', help='Ścieżka do pliku wejściowego')
parser.add_argument('output_file', help='Ścieżka do pliku wyjściowego')
parser.add_argument('--format', choices=['json', 'yaml', 'xml'], help='Format pliku wyjściowego')

# Parsowanie argumentów
args = parser.parse_args()
input_file = args.input_file
output_file = args.output_file
format = args.format

# Obsługa formatów plików
if input_file.endswith('.json'):
    with open(input_file, 'r') as j:
        try:
            data = json.load(j)
        except json.JSONDecodeError as e:
            print("Błąd w parsowaniu pliku JSON: ", e)
            exit(1)

elif input_file.endswith('.yml') or input_file.endswith('.yaml'):
    with open(input_file, 'r') as y:
        try:
            data = yaml.safe_load(y)
        except yaml.YAMLError as e:
            print("Błąd w parsowaniu pliku YAML: ", e)
            exit(1)

elif input_file.endswith('.xml'):
    with open(input_file, 'r') as f:
        xml_data = f.read()
        try:
            data = xmltodict.parse(xml_data)
        except Exception as e:
            print(f'Błąd odczytu pliku XML: {e}')
            exit(1)
else:
    print("Nieobsługiwany format pliku wejściowego: ", input_file)
    exit(1)

# Konwersja danych i zapis do pliku wyjściowego
if format == "json":
    with open(output_file, 'w') as j:
        json.dump(data, j, indent=4, sort_keys=True)

elif format == "yml" or format == "yaml":
    with open(output_file, 'w') as y:
        yaml.dump(data, y, default_flow_style=False)

elif format == "xml":
    try:
        def dict_to_xml(data, root):
            if isinstance(data, dict):
                for key, value in data.items():
                    child = ET.SubElement(root, key)
                    dict_to_xml(value, child)
            elif isinstance(data, list):
                for item in data:
                    dict_to_xml(item, root)
            else:
                root.text = str(data)

        root = ET.Element('data')
        dict_to_xml(data, root)
        tree = ET.ElementTree(root)
        xml_string = ET.tostring(root, encoding='utf-8')
        dom = xml.dom.minidom.parseString(xml_string)
        formatted_xml = dom.toprettyxml(indent="  ")

        with open(output_file, 'w') as f:
            f.write(formatted_xml)

    except Exception as e:
        print(f'Błąd zapisu pliku XML: {e}')
        exit(1)

else:
    print("Nieobsługiwany format pliku wyjściowego:", format)
    exit(1)

print("Konwersja zakończona powodzeniem")
