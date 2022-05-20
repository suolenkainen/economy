#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

## utilities.py
## Functions that are commonly used in modules.

import math
import ast



# Configuration data to a list of attributes tool
def conf_data_to_attribute_list(line):

    # split the data row into text form attributes
    data = line.strip().split(";")
    
    # For each attribute in the line, divide it into parameteds and add them to object as object attributes
    for i, d in enumerate(data):
        attr = d.strip().split("=")
        try:
            attr[1] = int(attr[1])
        except:
            try:
                attr[1] = float(attr[1])
            except:
                pass

        # For dicts and lists, use literal eval to transform string into appropriate data type
        if attr[0] in ["marketsell", "marketbuy", "goods", "producers", "workers", \
                    "workorders", "requirements", "sell", "resourcegoods", "storedresources"]:
            attr[1] = ast.literal_eval(attr[1])
        
        data[i] = attr
    
    return data



# Distance and angle between two settlements
def distance_calculator(a, b):
    (xa, ya) = a
    (xb, yb) = b

    x = abs(xa-xb)
    y = abs(ya-yb)

    # return the distance of points and clockwise angle in rads
    distance = round(math.sqrt(x*x + y*y))
    rads = math.atan2(yb-ya, xb-xa)

    return distance, rads



# Update worker coordinates so that the marker can be drawn to the game screen
def update_worker_coordinates(worker):

    y = worker.speed * math.sin(worker.angle)
    x = worker.speed * math.cos(worker.angle)

    worker.coordx += x
    worker.coordy += y



def endpoint_calculator(searched_object, sett_objects, param):

    # Find the endpoint 
    s_var = searched_object.__dict__[param]
    for d_var in sett_objects:
        if d_var.id == s_var:
            match = d_var
            break

    return match.coordx, match.coordy



if __name__ == "__main__":
    pass


