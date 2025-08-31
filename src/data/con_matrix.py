import pandas as pd
import numpy as np

def connections_to_locations(community, connection):
    """
    Convert port-level connectivity to community-level connectivity.
    """
    port_to_location = {}
    for location, ports in community.items():
        for port in ports:
            port_to_location[port] = location

    location_connections = {}
    for key, value in connection.items():
        port1, port2 = key.split(',')
        loc1 = port_to_location.get(port1.strip(), None)
        loc2 = port_to_location.get(port2.strip(), None)

        if loc1 and loc2:
            sorted_locs = tuple(sorted([loc1, loc2]))
            location_connections[sorted_locs] = location_connections.get(sorted_locs, 0) + value

    # Format back to dict "loc1,loc2": volume
    formatted_connections = {
        f"{loc1},{loc2}": flow for (loc1, loc2), flow in location_connections.items()
    }
    return formatted_connections


def connection_matrix(connection, community):
    """
    Create binary and volume connection matrices between communities.
    """
    locations = list(community.keys())
    matrix_zero = np.zeros((len(locations), len(locations)), dtype=int)
    
    matrix_binary = pd.DataFrame(matrix_zero.copy(), index=locations, columns=locations)
    matrix_volume = pd.DataFrame(matrix_zero.copy(), index=locations, columns=locations)
    
    for con, vol in connection.items():
        dep, ari = con.split(',')
        if dep in locations and ari in locations:
            matrix_binary.loc[dep, ari] = 1
            matrix_binary.loc[ari, dep] = 1
            matrix_volume.loc[dep, ari] = vol
            matrix_volume.loc[ari, dep] = vol
    
    return matrix_binary, matrix_volume