import json
import yaml
import xml.etree.ElementTree as ET
import xmltodict

print('Konwerter plików json, xml, yaml')

while True:
    
    # pobranie nazwy pliku wejściowego
    input_file = input("Podaj nazwę pliku wejściowego: ")

    # pobranie nazwy pliku wyjściowego
    output_file = input("Podaj nazwę pliku wyjściowego: ")

    format = output_file.split('.')[-1].lower()

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

    if format == "json":
        with open(output_file, 'w') as j:
            json.dump(data, j, indent=4, sort_keys=True)

    elif format == "yml" or format == "yaml":
        with open(output_file, 'w') as y:
            yaml.dump(data, y, default_flow_style=False)

    elif format == "xml":
        try:
            root = ET.Element('data')
            for key, value in data.items():
                child = ET.SubElement(root, key)
                child.text = str(value)
            tree = ET.ElementTree(root)
            tree.write(output_file, encoding='utf-8', xml_declaration=True)

        except Exception as e:
            print(f'Błąd zapisu pliku XML: {e}')
            exit(1)

    else:
        print("Nieobsługiwany format pliku wyjściowego:", format)
        exit(1)

    print("Konwersja zakończona powodzeniem")
    
    taknie = input('Chcesz konwertować dalej? (y/n)')
    if taknie == 'y':
        continue
    elif taknie == 'n':
        break
