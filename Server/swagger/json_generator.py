"""
Waits for RestAPI to start
Then collects help functions
And generates a new swagger.json file!
"""
import requests


url="http://localhost:8000"

# Wait for api is up
# Update fail response some times to let gui know we could not connect and so on...

# send get help for post, put and get!
json = {'func': 'help'}
print("----- Sending help request to get ----- ")
response = requests.get(url, params=json)
print(response.text)
print("----- Sending help request to post ----- ")
response = requests.post(url, data=jsonlib.dumps(json))
print(response.text)
print("----- Sending help request to put ----- ")
headers = {'Content-Type': 'html/text'}
response = requests.put(url, headers=headers, data=b'not empty', params=json)
print(response.text)

# Get Templates


# Create output for received objects!


# Create final file

# Move final file

# return success or fail