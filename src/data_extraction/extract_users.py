import os
import sys
sys.path.append('../../')

import tweepy
import json
import yaml

import math
from tqdm import tqdm

MAIN_DIR = '../../'
FOLLOWER_FNAME = 'followers'
USER_FNAME = 'users.json'

def extract_user_information(config_path):
    #load config file
    assert os.path.exists(config_path)

    with open(config_path) as file:
        config = json.load(file)


    #----------------------------------------------------------------
    #authenticate to Twitter API
    #----------------------------------------------------------------
    def find_keyfile(directory="."):
        """
        Helper function: Find the keyfile in a list of possible locations.
        The function iterates recursively through the directory and
        its subdirectories, emitting full paths for matching files.

        :returns: generator for keyfile paths
        """
        for root, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if filename == 'keys_0.yaml':
                    yield os.path.join(root, filename)
                

    try:
        filepath = next(find_keyfile())
    except StopIteration:
        raise Exception("No Keyfile found - please place keys.yaml with your tokens in the project directory or pass a custom filepath to the authorize() function")
    # Load credentials from keyfile
    with open(filepath, 'r') as f:
        keys = yaml.safe_load(f)

    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])  
    auth.set_access_token(config['access_token'], config['access_token_secret'])  

    api = tweepy.API(auth, wait_on_rate_limit=True)

    #----------------------------------------------------------------

    #load list of users to be extracted
    followers_list = []
    for line in open(os.path.join(MAIN_DIR, config["follower_fname"])):
        if line.strip():           # line contains eol character(s)
            n = int(line)
            followers_list.append(n)

    #get user information for each user in list
    with tqdm(total=len(followers_list)) as progress_bar:
        for userID in followers_list:
            try :
                print("Number {} with userID {}".format(i, userID))
                user = api.get_user(userID)
                all_users.append(user._json)
                
            except tweepy.error.TweepError:
                #e.g. when user doesn't exist anymore
                print('\nCaught TweepError exception' )

    all_user_json = {}
    for user in all_users:
        all_user_json[user["id"]] = user

    #save extracted user information
    with open(os.path.join(MAIN_DIR + config['data_dir'], USER_FNAME), 'w') as f:
        json.dump(all_user_json, fp, indent=4)

if __name__ == '__main__':
    config_path = sys.argv[1]
    
    extract_user_information(config_path)
