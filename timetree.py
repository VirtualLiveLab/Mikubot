import urllib.request
import json
import datetime
import discord
import Keys
from pprint import pprint

keyAPI = Keys.RetKEY("TimeTree2022")
# calenderID = '2FetEotw8UeF'  # 2021
calenderID = 'oYuKQ3sxKCyn'  # 2022


def getEventFromAPI():
    url = 'https://timetreeapis.com/calendars/{}/upcoming_events?timezone=Asia/Tokyo'.format(
        calenderID.join(calenderID.split()))
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'Bearer ' + keyAPI)
    req.add_header('Accept', 'application/vnd.timetree.v1+json')
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode('UTF-8'))
    pprint(data)
    return data


def getEventStartAt(content):
    s = str((int(content['attributes']['start_at'][11:16].replace(':', '')) + 900) % 2400)
    if len(s) == 3:
        return "0" + s[0:1] + ":" + s[1:3]
    else:
        return s[0:2] + ":" + s[2:4]


def getEventEndAt(content):
    s = str((int(content['attributes']['end_at'][11:16].replace(':', '')) + 900) % 2400)
    if len(s) == 3:
        return "0" + s[0:1] + ":" + s[1:3]
    else:
        return s[0:2] + ":" + s[2:4]


# イベントの名前を返す
def getEventTitle(content):
    return content['attributes']['title']


# その日のイベントを取得し、一覧にした文字列を返す
def getTodaysEvents(title):
    data = getEventFromAPI()
    todaysEvents = ''
    # 予定の件数を取得
    todaysEventsTop = '{}月{}日の予定は{}件だよ!\n\n'.format(datetime.date.today().month, datetime.date.today().day,
                                                    len(data['data']))
    embed = discord.Embed(title=title, description=todaysEventsTop, color=0x5efceb)

    # 予定のタイトルを取得し表示
    for content in data['data']:
        emName = getEventTitle(content)
        emValue = ''
        if content['attributes']['all_day']:
            emValue = '終日\n'
        else:
            emValue = (getEventStartAt(content) + '〜' + getEventEndAt(content) + '\n')
        embed.add_field(name=emName, value=emValue, inline=False)
    return embed


def getTodaysEventsJson(title):
    data = getEventFromAPI()
    todaysEvents = ''
    # 予定の件数を取得
    todaysEventsTop = '{}月{}日の予定は{}件だよ!\n\n'.format(datetime.date.today().month, datetime.date.today().day,
                                                    len(data['data']))
    embed = discord.Embed(title=title, description=todaysEventsTop, color=0x5efceb)

    # 予定のタイトルを取得し表示
    for content in data['data']:
        emName = getEventTitle(content)
        emValue = ''
        if content['attributes']['all_day']:
            emValue = '終日\n'
        else:
            emValue = (getEventStartAt(content) + '〜' + getEventEndAt(content) + '\n')
        embed.add_field(name=emName, value=emValue, inline=False)
    return embed
