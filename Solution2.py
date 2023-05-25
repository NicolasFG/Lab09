import requests
import json

x = input("Ingrese lugar: ")
place = requests.get("https://nominatim.openstreetmap.org/search?q={0}%20lima&format=json".format(x))
place_json = json.loads(place.text)
lat = place_json[0]["lat"]
lng = place_json[0]["lon"]

clima = requests.get("https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&forecast_days=2&daily=temperature_2m_max&timezone=PST".format(lat=lat,lng=lng))
clima_json = json.loads(clima.text)
clima_next_day = clima_json["daily"]["temperature_2m_max"][1]

lat2 = str(float(lat) + 0.01)
lng2 = str(float(lng) + 0.01)
restaurantes_cercanos = requests.get("https://api.openstreetmap.org/api/0.6/map.json?bbox={lng},{lat},{lng2},{lat2}".format(lng=lng,lat=lat,lng2=lng2,lat2=lat2))
restaurantes_json = json.loads(restaurantes_cercanos.text)

cnt=0
array=[]
for ele in restaurantes_json["elements"]:
    if (ele["type"]=="node" and cnt<3):
        if ("tags" in ele):
            s = ele["tags"]
            if("amenity" in s):
                y = ele["tags"]["amenity"]
                if (y=="restaurant"):
                    array.append(ele["tags"]["name"])
                    cnt +=1

print("Lugar: "+x)
print("Temperatura: " + str(clima_next_day))
print("Restaurantes")
for i in array:
    print(i)