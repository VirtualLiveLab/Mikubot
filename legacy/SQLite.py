import sqlite3
import discord
from pprint import pprint
# ----------------DB---------------
# 起動時、DBが存在しなかったら作成
dbname = 'IDchaine.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS ID(id INTEGER PRIMARY KEY AUTOINCREMENT, text_id INTEGER, role_id INTEGER)')


def set_id(t_id, r_id):
    sql = 'insert into ID (text_id, role_id) values (?,?)'
    idlist = (t_id, r_id)
    cur.execute(sql, idlist)
    conn.commit()


def del_id(d_id):
    sql = 'delete from ID where id = ?'
    deli = (str(d_id),)
    cur.execute(sql, deli)
    conn.commit()


def listall():
    cur.execute('select * from ID')
    result = cur.fetchall()
    return result


def out(search):
    try:
        where = 'select * from ID where text_id = ?'
        tapuru = (str(search),)
        cur.execute(where, tapuru)
        result = cur.fetchone()
        # print(result)
        ini, text_id, role_id = result
        # print(text_id)
        # print(role_id)
        return role_id

    except:
        print("Unknown ID")
        return -1

def makeids(x):
    rep = ""
    for i in listall():
        rep += str(i[x]) + "\n"
    print(rep)
    return rep

def makeDBembed():
    if makeids(0) != "":
        pprint(listall())
        embed = discord.Embed(title="DataBase")
        embed.add_field(name="id", value=makeids(0))
        embed.add_field(name="text_id", value=makeids(1))
        embed.add_field(name="role_id", value=makeids(2))
        return embed

    else:
        embed = discord.Embed(title="DataBase", description="error!\nデータベースの中身が存在しません", color=0xff0000)
        return embed

print(listall())
