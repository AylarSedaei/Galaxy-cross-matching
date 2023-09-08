from astropy.coordinates import SkyCoord
from astropy import units as u
from time import time

def crossmatch_tree(coords1, coords2):
    start_time = time()
    max_radius = 5
    matches = []
    no_matches = []
    
    # Convert to astropy coordinates objects
    coords1_sc = SkyCoord(coords1*u.degree, frame='icrs')
    coords2_sc = SkyCoord(coords2*u.degree, frame='icrs')
    
    # Perform crossmatching
    closest_ids, closest_dists, _ = coords1_sc.match_to_catalog_sky(coords2_sc)
    
    for id1, (closest_id2, dist) in enumerate(zip(closest_ids, closest_dists)):
        closest_dist = dist.value
        # Ignore match if it's outside the maximum radius
        if closest_dist > max_radius:
            no_matches.append(id1)
        else:
            matches.append([id1, closest_id2, closest_dist])
    
    time_taken = time() - start_time
    return matches, no_matches, time_taken