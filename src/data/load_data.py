import json

def data_loader(path, ):
    
    # Read the JSON file
    with open(path, 'r') as file:
        df = json.load(file)
    return df