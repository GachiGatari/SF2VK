import requests
import configparser
import vk_api
import vk_api.vk_api
import time


config = configparser.ConfigParser()
config.read("settings.ini")
token_vk = config["VK"]["TOKEN"]
client_id = config["SPOTIFY"]["CLIENT_ID"]
client_secret = config["SPOTIFY"]["CLIENT_SECRET"]
base64 = config["SPOTIFY"]["BASE64"]
refresh_token = config["SPOTIFY"]["REFRESH_TOKEN"]
vk = vk_api.VkApi(token=token_vk)


def get_token():
    headers = {
        "Authorization" : f"Basic {base64}"
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': f'{refresh_token}',
    }
    response = requests.post('https://accounts.spotify.com/api/token',data=data,headers=headers)
    return  response.json()["access_token"]



def convertMillis(millis):
    seconds=((millis/1000)%60)
    minutes=((millis/(1000*60))%60)%10

    return f"{str(minutes)[:1]}:{str(round(seconds))[:2]}"

def get_current_music():
    headers = {
        "Accept":"application/json",
        "Content-Type":"application/json",
        "Authorization":f"Bearer {get_token()}"
    }

    response = requests.get("https://api.spotify.com/v1/me/player/currently-playing",headers=headers)
    curr_music = response.json()
    icon = "⏺" if curr_music['is_playing'] else "⏸"
    status = f"Сейчас слушает: {curr_music['item']['name']}__({curr_music['item']['artists'][0]['name']}) " \
             f" {convertMillis(curr_music['progress_ms'])}/{convertMillis(curr_music['item']['duration_ms'])}" \
             f"{icon}" \
             f"&#12288;&#12288;&#12288;&#12288;&#12288;&#12288;&#12288;&#12288;&#12288;&#12288;&#12288;&#12288;&#12288;&#12288;&#12288;{curr_music['item']['external_urls']['spotify']}"
    return status

def set_status():
    data = {"text":get_current_music()}
    response = vk.method("status.set",data)




def run():
    while True:
        set_status()
        time.sleep(60)

if __name__ == "__main__":
    run()