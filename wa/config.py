import yaml

def read(filename: str):
    with open(f'config/{filename}.yml', 'r', encoding='utf8') as file:
        return yaml.load(file, Loader=yaml.FullLoader)
