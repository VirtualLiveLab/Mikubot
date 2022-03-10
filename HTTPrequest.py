import requests
import Keys
from pprint import pprint

# url = "https://timetreeapis.com/calendars/oYuKQ3sxKCyn/upcoming_events?timezone=Asia/Tokyo" #TimeTree_VLL2022
# url = "https://discord.com/api/v8/guilds/938738282710335559/members?limit=10"
# url = "https://discord.com/api/webhooks/950259048668856380/YyMsU_-JqLuhlX86LXc7YaBrLpZ8p3gSdbHM_JZUHQgJaIh9WuXjivNj4g7VcwIGmn4r"

# headers = {
#     "Accept": "application/vnd.timetree.v1+json",
#     "Authorization": "Bearer " + Keys.RetKEY("TimeTree2022")
# }

# headers = {
#     "Authorization": "Bot " + Keys.RetKEY("VLL2022TOKEN") # Practice
# }

json = {
    "content": "https://www.youtube.com/watch?v=ty9-Rjlv5zc",
    "files": "./README.md"
}


r = requests.post(url, json=json)
# r = requests.get(url, headers=headers)
# r = requests.put(url, headers=headers, json=json)
# r = requests.delete(url, headers=headers)

pprint(r)