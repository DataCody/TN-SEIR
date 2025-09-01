import numpy as np

def infection(α, β, γ, community_seir):
    """
    Simulate the infection process within each community based on the SEIR model.

    Args:
        α (float): Transmission rate, the probability of susceptible individuals becoming exposed.
        β (float): Recovery rate, the probability of infected individuals recovering.
        γ (float): Progression rate, the probability of exposed individuals becoming infectious.
        community_seir (pd.DataFrame): A DataFrame containing the SEIR values for each community,
                                       indexed by community names with columns for 'S', 'E', 'I', 'R' and their ratios.

    Returns:
        pd.DataFrame: Updated DataFrame after applying the infection dynamics to each community.
    """
    # Create a copy to update the community SEIR values without altering the original during iteration
    updated_seir = community_seir.copy()
    
    for index, row in updated_seir.iterrows():
        if index != 'Outside World':  # Skip "Outside World"
            n = row['S'] + row['E'] + row['I'] + row['R']
            if n > 0:
                S, E, I, R = row['S'], row['E'], row['I'], row['R']
                δ_SE = np.random.binomial(S, α * I / n if I > 0 else 0)  # Susceptible to Exposed
                δ_EI = np.random.binomial(E, γ)  # Exposed to Infected
                δ_IR = np.random.binomial(I, β)  # Infected to Recovered
                
                # Update the SEIR counts
                updated_seir.at[index, 'S'] = S - δ_SE
                updated_seir.at[index, 'E'] = E + δ_SE - δ_EI
                updated_seir.at[index, 'I'] = I + δ_EI - δ_IR
                updated_seir.at[index, 'R'] = R + δ_IR

                # Update the ratios
                #total_pop = updated_seir.at[index, 'S'] + updated_seir.at[index, 'E'] + updated_seir.at[index, 'I'] + updated_seir.at[index, 'R']
                updated_seir.at[index, 'S_ratio'] = updated_seir.at[index, 'S'] / updated_seir.at[index, 'Population']
                updated_seir.at[index, 'E_ratio'] = updated_seir.at[index, 'E'] / updated_seir.at[index, 'Population']
                updated_seir.at[index, 'I_ratio'] = updated_seir.at[index, 'I'] / updated_seir.at[index, 'Population']
                updated_seir.at[index, 'R_ratio'] = updated_seir.at[index, 'R'] / updated_seir.at[index, 'Population']
    
    return updated_seir