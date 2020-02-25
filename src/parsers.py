import json

with open('Locations.json') as fil:
    data = json.load(fil)

# js = {}
# for key in data:
#     js[key] = {
#         "type": data[key][0],
#         "latlng": []
#     }

js = []
for key in data:
    js.append ({
        "name": key,
        "type": data[key][0],
        "latlng": []
    })


with open('Locations-Mine.json', 'w') as fil:
    json.dump(js, fil)