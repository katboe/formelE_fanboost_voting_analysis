# Twitter Analysis of FormelE's Fanboost Voting
In Formel-E fans can vote for their favorite driver via Twitter and the official Fanboost website in order to enable a special boost during the race called fanboost. The boost can be of help in overtaking maneuvers. The voting is enabled for 10 days prior to a race and the player with the most votes gets the fanboost.

In this project we analyse the Twitter fanboost votings of Formel-E races in 2018/19. We first extract voting tweets from Twitter using tweep, construct voting networks and analyse the networks using the network analysis tool 'visone'.

## Data Extraction
Tweets count as fanboost vote if they are created within 10 days before a race and contain the hashtag "#fanboost" together with the driver's twitter screenname as hashtag or user mention. 

Extracting tweets by hashtags via the Twitter API is very costly. Hence, instead searching for hashtags, we construct a set of twitter users, that have potentially voted for a driver, and search their tweet archives for tweets meeting the voting criteria. For this, we assume that all fanboost voters are fans of Formel-E and therefore follow the official Twitter account of Formel-E ('fiaformulae'). Hence, our approach for data extraction is:

1. Extract follower ids of official Twitter account of Formel-E: 
    
    ```src/data_extraction/extract_follower_ids.py ../../config/config.json```

2. For each follower: Extract tweet archive (contains last 2500 tweets)

   This process is designed to be exectued multiple times in parallel in order to speed up the process if multiple twitter access keys are available.
   
    ```src/data_extraction/extract_follower_tweets.py ../../config/config.json {process_id}```

3. For each follower: Extract user information
    
   ```src/data_extraction/extract_user_information.py ../../config/config.json```
   
 
## Data Preparation
1. Prepare user information: Determine country of user location, if available. 
  Since user information is entered manually in a free text field, the information is not too reliable though.

2. Construct voting network as networkx multi-graph and save as .graphml for analysis: 
  If a tweet was created within 10 days prior to a race, an edge is added from the user-node to the driver-node. Hence, the network contains two types of nodes: twitter-user and driver nodes. Nodes contain attributes such as twitter user ids, screen names and user locations/country. 

## Data Analysis

Load graphs into software 'visone' for visualisation, clustering, etc. 
