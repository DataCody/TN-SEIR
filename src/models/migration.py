import pandas as pd
import numpy as np


def migration(community_seir, binary_matrix, volume_matrix, inbound):
    communities = community_seir.index
    migration_df = pd.DataFrame(0, index=communities, columns=['S_out', 'E_out', 'I_out', 'R_out', 'S_in', 'E_in', 'I_in', 'R_in'])

    for source in communities:
        for target in communities:
            if source != target and binary_matrix.loc[source, target] == 1:
                if source == 'Outside World':
                    # Random inbound population between the specified bounds
                    P = np.random.randint(inbound[0], inbound[1] + 1)
                    E = int(P * inbound[2])
                    S = P - E
                    I, R = 0, 0
                    max_migrants = P

                    # Ensure we do not exceed the available population in "Outside World"
                    max_migrants = min(max_migrants, community_seir.loc['Outside World', ['S', 'E', 'I', 'R']].sum())
                    selected_counts = pd.Series({'S': S, 'E': E, 'I': I, 'R': R})

                    for seir_type in ['S', 'E', 'I', 'R']:
                        migrants_count = selected_counts.get(seir_type, 0)
                        migration_df.loc[source, seir_type + '_out'] += migrants_count
                        migration_df.loc[target, seir_type + '_in'] += migrants_count
                        community_seir.loc[source, seir_type] -= migrants_count
                        community_seir.loc[target, seir_type] += migrants_count

                    # Randomly select SEIR individuals to return to "Outside World"
                    total_migrants_back = sum(selected_counts.values)
                    available_seir = community_seir.loc[target, ['S', 'E', 'I', 'R']].clip(lower=0)
                    repeats = available_seir.astype(int).values
                    population_indices = np.repeat(['S', 'E', 'I', 'R'], repeats)

                    if total_migrants_back > len(population_indices):
                        total_migrants_back = len(population_indices)

                    selected_indices = np.random.choice(population_indices, size=total_migrants_back, replace=False)
                    selected_counts_back = pd.Series(selected_indices).value_counts()

                    for seir_type in ['S', 'E', 'I', 'R']:
                        migrants_count = selected_counts_back.get(seir_type, 0)
                        migration_df.loc[target, seir_type + '_out'] += migrants_count
                        migration_df.loc[source, seir_type + '_in'] += migrants_count
                        community_seir.loc[target, seir_type] -= migrants_count
                        community_seir.loc[source, seir_type] += migrants_count

                elif target == 'Outside World':
                    # No need to handle separately as it's symmetric to above

                    pass
                else:
                    max_migrants = int(volume_matrix.loc[source, target] * 0.8)
                    available_seir = community_seir.loc[source, ['S', 'E', 'I', 'R']].clip(lower=0)
                    total_available = available_seir.sum()
                    
                    if total_available > 0 and max_migrants > 0:
                        max_migrants = min(int(max_migrants), int(total_available))
                        
                        repeats = available_seir.astype(int).values
                        population_indices = np.repeat(['S', 'E', 'I', 'R'], repeats)
                        
                        if max_migrants > len(population_indices):
                            max_migrants = len(population_indices)
                        selected_indices = np.random.choice(population_indices, size=max_migrants, replace=False)
                        
                        selected_counts = pd.Series(selected_indices).value_counts()
                        
                        for seir_type in ['S', 'E', 'I', 'R']:
                            migrants_count = selected_counts.get(seir_type, 0)
                            migration_df.loc[source, seir_type + '_out'] += migrants_count
                            migration_df.loc[target, seir_type + '_in'] += migrants_count
                            community_seir.loc[source, seir_type] -= migrants_count
                            community_seir.loc[target, seir_type] += migrants_count

    community_seir['S_ratio'] = community_seir['S'] / community_seir['Population']
    community_seir['E_ratio'] = community_seir['E'] / community_seir['Population']
    community_seir['I_ratio'] = community_seir['I'] / community_seir['Population']
    community_seir['R_ratio'] = community_seir['R'] / community_seir['Population']
    
    return community_seir, migration_df