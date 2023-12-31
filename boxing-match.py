import numpy as np
from time import time

def angular_dist_rad(r1, d1, r2, d2):
    deltar = np.abs(r1 - r2)
    deltad = np.abs(d1 - d2)
    angle = 2*np.arcsin(np.sqrt(np.sin(deltad/2)**2 
                        + np.cos(d1)*np.cos(d2)*np.sin(deltar/2)**2))
    return angle

def crossmatch_box(coords1, coords2):
    start_time = time()
    deg2rad = np.pi/180
    rad2deg = 180/np.pi
    max_radius = 5*deg2rad
    matches = []
    no_matches = []
    
    # Convert coordinates to radians
    coords1 = coords1*deg2rad
    coords2 = coords2*deg2rad
    
    # Find ascending declination order of second catalogue
    asc_dec = np.argsort(coords2[:, 1])
    coords2_sorted = coords2[asc_dec]
    dec2_sorted = coords2_sorted[:, 1]
    
    for id1, (ra1, dec1) in enumerate(coords1):
        closest_dist = np.inf
        closest_id2 = None
        
        # Declination search box
        min_dec = dec1 - max_radius
        max_dec = dec1 + max_radius
        
        # Start and end indices of the search
        start = dec2_sorted.searchsorted(min_dec, side='left')
        end = dec2_sorted.searchsorted(max_dec, side='right')
        
        for s_id2, (ra2, dec2) in enumerate(coords2_sorted[start:end+1], start):
            dist = angular_dist_rad(ra1, dec1, ra2, dec2)
            if dist < closest_dist:
                closest_sorted_id2 = s_id2
                closest_dist = dist
        
        # Ignore match if it's outside the maximum radius
        if closest_dist > max_radius:
            no_matches.append(id1)
        else:
            closest_id2 = asc_dec[closest_sorted_id2]
            matches.append([id1, closest_id2, closest_dist*rad2deg])
    
    time_taken = time() - start_time
    return matches, no_matches, time_taken