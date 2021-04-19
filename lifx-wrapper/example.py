from api import LifxAPI
import secret, random

# Enter your own api_key here
API_KEY = secret.API_TOKEN

api = LifxAPI(API_KEY)

# Toggle the power of all your lights
api.toggle_power()

# Get all Lights in json format
lights = api.list_lights()

ids = []

# Get all lamp ID's in your account
for light in lights:
    ids.append(light["id"])

# Set all lamps in your account to a random brightness (between 0.0 and 1.0)
# Note: When fast is enabled you get no API response.
for id in ids:
    api.set_state(selector=f"id:{id}", brightness=(random.randint(0, 100) / 100), fast=True)
