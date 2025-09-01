import json

def load_data(json_path):
    """
    Load and parse the JSON file containing connectivity and community information.

    Args:
        json_path (str): Path to the JSON file.
    
    Returns:
        dict: population (community -> population size)
        dict: community (community -> ports)
        dict: connection (port-pair -> volume)
    """
    with open(json_path, 'r') as file:
        df = json.load(file)
    
    connection = df['Connectivity Matrix W'].copy()
    community = df['ports_according_communities'].copy()
    n = df['n'].copy()

    # Extract outside world population separately
    outside_world = {'Outside World': n.pop('Outside World')}
    sorted_data = {k: n[k] for k in sorted(n)}
    population = {**outside_world, **sorted_data}

    return population, community, connection