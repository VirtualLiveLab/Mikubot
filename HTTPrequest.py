import requests
import Keys
from pprint import pprint

url = "https://timetreeapis.com/calendars/oYuKQ3sxKCyn/upcoming_events?timezone=Asia/Tokyo" #TimeTree_VLL2022

headers = {
    "Accept": "application/vnd.timetree.v1+json",
    "Authorization": "Bearer " + Keys.RetKEY("TimeTree2022")
}

# json = {
#
# }

# r = requests.post(url, headers=headers, json=json)
r = requests.get(url, headers=headers)
# r = requests.put(url, headers=headers, json=json)
# r = requests.delete(url, headers=headers)

pprint(r.json())