from gaspricefunctions import getAddressGasStation
import requests



lat="4385400" 
lon="1.22800"

lat = lat[0:2] + '.' + lat[2:]
lat = str(lat)

print(lat)

url = 'https://api-adresse.data.gouv.fr/reverse/?lon=' + lon + '&lat=' + lat
resp = requests.get(url)

print(resp)


"""
address = getAddressGasStation(lon,lat)
print(address)
"""