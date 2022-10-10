import os
import sys
sys.path.append('../../')

import tweepy
import json
import yaml

import math
from datetime import date
from tqdm import tqdm

SCREEN_NAME = 'fiaformulae'
MAIN_DIR = '../../'
FOLLOWER_FNAME = 'followers'


def extract_followers(config_path):
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


    #get ser stats for progress bar
    user = api.get_user(screen_name=SCREEN_NAME)
    num_followers = user.followers_count
    num_followers = 15000
    page_size = 5000
    num_pages = math.ceil(num_followers / page_size)

    #extract follower ids (waits when Twitter API rate limit is reached)
    followers_list = [] 
    with tqdm(total=num_pages) as progress_bar:
        for page in tweepy.Cursor(api.get_follower_ids, screen_name= SCREEN_NAME, count=page_size).pages(3):
            followers_list += page
            progress_bar.update(1) 
        
    print(f"Count of extracted followers {len(followers_list)}")

    #save follower ids
    with open(os.path.join('../../' + config['data_dir'], f"{FOLLOWER_FNAME}_{date.today().strftime('%Y-%m-%d')}.txt"), 'w') as f:
        for item in followers_list:
           f.write("%s\n" % item)


if __name__ == '__main__':
    config_path = sys.argv[1]
    
    extract_followers(config_path)
