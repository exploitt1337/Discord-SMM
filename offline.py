import os, sys
import requests
import  json
import time
from threading import Thread
import ctypes
import time
API_ENDPOINT = 'https://canary.discord.com/api/v9'
CLIENT_ID = '1089980309799444550'
CLIENT_SECRET = ""
REDIRECT_URI = 'https://verify.exploit.tk'
tkn = "MTEyMzk0Njg0OTg4ODM3NDgxNg.GYzZOE.fuPGQTsrz75GRxI0SHaXKLOuV1qyzMai7JpHDE"

def get_members(guild_id):
    scraped = False
    url = f'https://canary.discord.com/api/v9/guilds/{guild_id}/members'
    headers = {
        'Authorization': f'Bot {tkn}'
    }

    members = []
    member_ids = []
    params = {
        'limit': 1000
    }

    while True:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            new_members = json.loads(response.text)
            members.extend(new_members)

            if len(new_members) < 1000:
                scraped = True
                break
            elif response.status_code == 429:
               if 'retry_after' in response.text:
                    sleep = response.json()['retry_after']
                    print("[DEBUG]: sleeping for:", sleep, "seconds")
                    time.sleep(sleep)
                    continue
               else:
                    break
            else:
                params['after'] = new_members[-1]['user']['id']
        else:
            print(f"Failed to retrieve guild members. Error: {response.text}")
            break
    
    if scraped:
        for member in members:
            member_ids.append(member['user']['id'])

        return member_ids
    else:
        return None
  
guild = input("guild: ")

starter = int(input("start from: "))
amount = input("amount: ")

members = get_members(guild)
def add_to_guild(access_token, userID , guild_Id, added):
    if userID in members:
        print(f"{added} [INFO]: user {userID} already in {guild_Id}")
        return "fail"
    while True:
        url = f"{API_ENDPOINT}/guilds/{guild_Id}/members/{userID}"

        botToken = tkn
        data = {
        "access_token" : access_token,
    }
        headers = {
        "Authorization" : f"Bot {botToken}",
        'Content-Type': 'application/json'

    }
        response = requests.put(url=url, headers=headers, json=data)
        # print(response.text)
        if response.status_code in (200, 201, 204):
          if "joined" not in response.text:
            print(f"[INFO]: user {userID} already in {guild_Id}")
            return "fail"
          print(f"{added} [INFO]: successfully added {userID} to {guild_Id}")
          return "success"
        elif response.status_code == 429:
          #  print(response.status_code)
          #  print(response.text)
           if 'retry_after' in response.text:
               sleepxd = response.json()['retry_after']
               print("sleeping for:", sleepxd, "seconds")
               time.sleep(sleepxd)
               continue
           else:
             os.system("kill 1")
        else:
           print(response.text)
           return "fail"
        break
f = open("offline.txt", "r").readlines()

if "all" in amount.lower():
  amount = int(len(open("offline.txt", "r").readlines()))
else:
  amount = int(amount)

print("AMOUNT:", amount)
xx = 0
added = 0 
errors = 0
start_time = time.time()
def title():
   speed = round(added / ((time.time() - start_time) / 60))
   ctypes.windll.kernel32.SetConsoleTitleW("Joined: %s | Errors: %s | Speed: %s/m" % (added, errors, speed))
for line in f:
  xx += 1
  if xx < starter: 
    continue 
  elif amount < added:
    sys.exit()
  line = line.strip()
  line = line.split(":")
  key = line[0]
  value = line[1]
  req = add_to_guild(value, key, guild, added)
  if req == "fail":
    errors += 1
    title()
    # print("failed")
    continue
  elif req == "success":
    # print("success")
    added += 1
    title()
    continue
  else:
    errors += 1
    title()
    # print("failed")
    continue

print("\n\nTotal Added: ", added)
