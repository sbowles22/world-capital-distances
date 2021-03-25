from math import radians, cos, sin, asin, sqrt
from pyexcel_ods import get_data
import json


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


data = get_data("capitals.ods")
data = data["Sheet1"][1:]

seen = set()
results = []
for i, c in enumerate(data):
    for j, d in enumerate(data):
        if (i, j) not in seen:
            if c[1][0] == d[1][0] and c[1] != d[1]:
                lon1 = float(c[3][:-1])
                lat1 = float(c[2][:-1])
                lon2 = float(d[3][:-1])
                lat2 = float(d[2][:-1])
                results.append((haversine(lon1, lat1, lon2, lat2), c[1], d[1]))

                results = sorted(results, key=lambda x: x[0], reverse=True)
        seen.add((i, j))
        seen.add((j, i))

for i in results:
    print(f'{i[1]} and {i[2]} are {round(i[0])}km apart')
