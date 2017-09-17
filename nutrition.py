## THIS WORKS FKING INCREDIBLYYYY

# 1000 requests per hour max
import requests

api_key = 'NOcQy0cMX1xfkw68ClTp6UiU7vttr8231es732rs'
query = 'banana'

# searches database for specific entries
r = requests.get('https://api.nal.usda.gov/ndb/search/?format=json&q=' + query + '&max=1&offset=0&api_key=' + api_key)
mostRelevantItemId = r.json()['list']['item'][0]['ndbno']

# finds details about most relevant entry found
infoAboutRelevantItem = requests.get('https://api.nal.usda.gov/ndb/reports/?ndbno=' + str(
    mostRelevantItemId) + '&type=f&format=json&api_key=' + api_key).json()

# get rid of bullcrap
nutrients = {nutrient['name']: str(nutrient['value']) + ' ' + str(nutrient['unit']) for nutrient in
             infoAboutRelevantItem['report']['food']['nutrients']}

print("Nutrient info for " + query + ":")
print(nutrients)  # <<<<<<<<<<<<<<<< gold.
