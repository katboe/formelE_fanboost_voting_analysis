import sys
sys.path.append('../../')
import os 

import rest
import json
import yaml

import math
from datetime import date
from tqdm import tqdm

MAIN_DIR = '../..'

def scrape(config_path, process_id):
	#load config
	assert os.path.exists(config_path)

	with open(config_path) as file:
	        config = json.load(file)


	#load extracted follower ids
	followers_list = []
	for line in open(os.path.join(MAIN_DIR, config["follower_fname"])):
	    if line.strip():           # line contains eol character(s)
	        n = int(line)
	        followers_list.append(n)


	#check validity of process_id
	if process_id >=  config["total_num_process"]:
		print(f"process_id has to be smaller than {config['total_num_process']}")
		sys.exit()

	#get to extractable part of follower ids list
	num_total = len(followers_list)
	len_per_process = math.ceil(num_total / config["total_num_process"])

	if process_id !=  config["total_num_process"] - 1:
	    curr_followers_list = followers_list[process_id*len_per_process:(process_id + 1)*len_per_process]
	else:
	    curr_followers_list = followers_list[process_id*len_per_process:]
	print(f"Number of accounts to be extracted: {len(curr_followers_list)}")

	#extract all tweets of followers containing #fanboost
	tweetsDict = dict()
	fanboostCount = 0

	for userid in curr_followers_list:
	    print(f'userid: {userid}')
	    try:
	        archive = rest.fetch_user_archive(userid)
	        tweetcount = 0
	        tweetlist = dict()
	        for page in archive:
	            for tweet in page:
	                #print(tweet['text'])
	                tweetcount = tweetcount + 1
	                fanboost = False
	                for hashtag in (tweet['entities'])['hashtags']:
	                    if hashtag['text'].lower() == "fanboost" :
	                        if not fanboost:
	                            fanboostCount = count + 1
	                            print(tweet)
	                            fanboost = True
	                            tweetlist[tweet["id"]] = tweet

	        if not tweetlist:
	            print(f"no fanboost tweet among {tweetcount} tweets")
	        else:
	            print("fanboost tweets detected")
	            tweetsDict[userid] = tweetlist
	            
	    except (RuntimeError, NameError, ValueError) as error:
	        print(error)
	        if error[0]['code'] == 34:
	            print("account deleted")
	        else:
	            errorCount = errorCount + 1
	            print("error")
	            print(error)
	        pass
	    except Exception as e:
	        print(e)
	        pass
	   
	tweet_path = os.path.join(MAIN_DIR, config['tweets_dir'])
	if tweetsDict != {}:
	    with open(os.path.join(tweet_path, f'tweets_{process_id}.json'), 'w') as fp:
	        json.dump(tweetsDict, fp, indent=4)


if __name__ == '__main__':
    config_path = sys.argv[1]
    process_id = int(sys.argv[2])

    scrape(config_path, process_id)