
import requests

request = "http://localhost:50001/" + "scripts/" + "sikuliscripts"
print(request)

r = requests.get(request)
print(r)