import pandas as pd

def seir_statement(day, community_seir): # inbound,
    """
    Updates or initializes the SEIR model states for a community with additional inbound effects.

    Args:
        day (int): Current simulation day. If day == 1, initialize the SEIR model.
        inbound (list): A list containing the minimum and maximum expected inbound individuals,
                        and the exposure rate among them.
        community (dict): A dictionary of communities with their initial populations.
        expose_rate (float): The rate at which inbound individuals are exposed to the disease.

    Returns:
        pd.DataFrame: A DataFrame containing updated SEIR values and ratios for each community.
    """
    
    # Initialize or copy the community DataFrame
    
    
    if day == 1:
        # Initial locations and population
        community_seir['Outside World'] = 0
        community_seir = pd.DataFrame(list(community_seir.values()), index=community_seir.keys(), columns=['Population'])
        # Initialize SEIR columns
        community_seir['S'] = community_seir['Population']
        community_seir['E'] = 0
        community_seir['I'] = 0
        community_seir['R'] = 0
    
    else:
        # Assume community_seir is already a DataFrame
        community_seir = community_seir.copy()
        
    # # Random inbound population between the specified bounds
    # P = np.random.randint(inbound[0], inbound[1] + 1)
    # E = int(P * inbound[2])  # Exposed individuals among inbound
    # S = P - E                # Susceptible individuals among inbound
    # I, R = 0, 0              # Initially, no infected or recovered in inbound

    # Update the 'Outside World' inbound directly in the DataFrame
        
    community_seir.loc['Outside World', 'Population'] = 0
    community_seir.loc['Outside World', 'S'] = 0
    community_seir.loc['Outside World', 'E'] = 0
    community_seir.loc['Outside World', 'I'] = 0
    community_seir.loc['Outside World', 'R'] = 0

    # Calculate the population ratios of S, E, I, and R
    community_seir['S_ratio'] = community_seir['S'] / community_seir['Population']
    community_seir['E_ratio'] = community_seir['E'] / community_seir['Population']
    community_seir['I_ratio'] = community_seir['I'] / community_seir['Population']
    community_seir['R_ratio'] = community_seir['R'] / community_seir['Population']
    

    return community_seir
