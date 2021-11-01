import requests
import json
from tweepy.api import API
import tweepy
from time import sleep
import colorama
from colorama import Fore , Back ,Style
from tweepy.error import TweepError
colorama.init()
import facebook
import os

file_path = "lightswitch.json"
with open ("your_tokens.json" , "r+") as token :
    tokens = json.load(token)

#TOKENS OF ALL [TWITTER AND FACEBOOK]
facebook_posting_token = tokens['facebook_token'] #PAGE TOKEN
consumer_key = tokens['API_key'] #TWITTER
consumer_secret_key = tokens['API_Secret_Key'] #TWITTER
access_token = tokens['Access_Token'] #TWITTER
access_token_secret = tokens['Access_Token_Secret'] #TWITTER
#######################################################################
auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)         #
auth.set_access_token(access_token, access_token_secret)              #
api = tweepy.API(auth)                                                #
#######################################################################

####################
def save_file_with_contents(path, contents):
    file = open(path, 'w')
    file.write(contents)
    file.close()
    return True
###############
def save_last(status, message):
    return save_file_with_contents(file_path, json.dumps({
        "status": status,
        "message": message,
    }, sort_keys=True, indent=4))
#################################
def check():
    lightswitch = ((requests.get('https://api.nitestats.com/v1/epic/lightswitch')).json())[0]
    lightswitch_old = json.loads((open(file_path, 'r').read())) 

    status = lightswitch['status']
    message = lightswitch['message']

    if lightswitch_old['status'] == status:
        print(Fore.LIGHTMAGENTA_EX)
        print(f'-> checking for change in fortnite servers (status) servers still {Fore.MAGENTA}{status} .') # Print checking message
        save_last(status, message)
    else:
        print("CHANGE DETECTED...")
        print(Fore.YELLOW)
        print(f'-> Fortnite servers is {Fore.LIGHTRED_EX}{status} NOW... ') # Print the change is detected to make the the posting
        print(Fore.LIGHTYELLOW_EX)
        print("-> tweeting FN status...")
        save_last(status,message)
        if status == "UP" :
            text = f"Fortnite Servers is {status} 🢁 "
        if status == "DOWN" :
            text = f"Fortnite Servers is {status} 🢃 \n\n• The Message :\n[{message}] "
        else :
            text = f"Fortnite Servers is {status} \n\n• The Message :\n[{message}] "
        img = f"{status}image.png"
        try :
            api.update_with_media(img,text)
            print(Fore.LIGHTGREEN_EX)
            print("-> FN status tweeted")
        except:
            print(f"{Fore.LIGHTRED_EX}-> Failed to tweet The status Please check your tokens (it's not working) ")

        
        if facebook_posting_token != "" :
            print(Fore.LIGHTYELLOW_EX)
            print("\n-> POSTING ON FACEBOOK...")
            try:
                token_user = facebook.GraphAPI(facebook_posting_token)
                token_user.put_photo(open(f'{status}image.png', 'rb') ,message=f"{text}")
                print(f"{Fore.LIGHTGREEN_EX}-> POSTED ON FACEBOOK")
            except:
                print(f"{Fore.LIGHTRED_EX}-> Failed to Post The status Please check your Page tokens (it's not right)")

        else :
            print("")
    sleep(15)

lolsame = "lol"
while True :
    try :
        check()
    except:
        print(f"{Fore.LIGHTRED_EX}\n-> ERORR :THERE'S PROBLEM : PLEASE CHECK YOUR INTERNET CONNECTION")
        sleep(15)
