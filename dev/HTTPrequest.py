import requests
from pprint import pprint
import time
# import json

# url = "https://timetreeapis.com/calendars/oYuKQ3sxKCyn/upcoming_events?timezone=Asia/Tokyo" #TimeTree_VLL2022
# url = "https://discord.com/api/v8/guilds/938738282710335559/roles"
url = "https://discord.com/api/v8/guilds/1089948443297992915/members?limit=500"


# headers = {
#     "Accept": "application/vnd.timetree.v1+json",
#     "Authorization": "Bearer " + Keys.RetKEY("TimeTree2022")
# }

headers = {
    "Authorization": "Bot" # Practice
}

# name = ["Hatsune","世界の真ん中を歩く","Hello, World!","MC1","フォニイ","ロウワー","グッバイ宣言","天ノ弱","スーパーヒーロー","T.A.O","MC2","孤独の果て","ビバハピ","えれくとりっく・えんじぇぅ","ルカルカ★ナイトフィーバー","on the rocks","MC3","エゴ","霽れを待つ","Last Night, Good Night","ファイヴ","MC4","ODDS & ENDS","アンコール","Catch the Wave","水色侵略","愛言葉Ⅱ","MC5","Connecting","39","ED","テーマ曲"]

# json = {
#     "role": 1107943462881468426
# }

# for r in name:

#     json = {
#         "name": r,
#         "mentionable": True
#     }


#     r = requests.post(url, headers=headers, json=json)

# # r = requests.put(url, headers=headers, json=json)
# # r = requests.delete(url, headers=headers)

r = requests.get(url, headers=headers)

list = []

for i in r.json():
    list.append(i["user"]["id"])

pprint(list)

for id in list:
    res = requests.put("https://discord.com/api/v8/guilds/1089948443297992915/members/" + id + "/roles/1107943462881468426", headers=headers)
    pprint(res)
    time.sleep(3)
