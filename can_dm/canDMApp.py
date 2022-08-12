# import the required libraries
import tweepy
import numpy as np
import pandas as pd

# to read the configuration file
import configparser


def get_api():
    """
    authenticate and connect with the twitter api using keys and tokens
    :return
        api: obeject of the tweepy api
    """
    # read the configuration file
    config = configparser.ConfigParser(interpolation=None)
    config.read("config.ini")
    API_KEY = config['twitter']["api_key"]
    API_KEY_SECRET = config['twitter']["api_key_secret"]
    ACCESS_TOKEN = config['twitter']["access_token"]
    ACCESS_TOKEN_SECRET = config['twitter']["access_token_secret"]

    # authenticate
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # initialize API
    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api

def main():
    """
    collects the data and save
    :return
        df: dataframe
    """
    # create api object
    client = get_api()

    # read urls
    df = pd.read_csv("twitter_profile_Sheet2.csv", header=None, names=["urls"])
    df["username"] = df['urls'].apply(lambda x: x.split("/")[-1])
    # empty list to hold can_dm status
    can_dm_list = []

    MY_ACCOUNT_NAME = "..."  # FILL THIS WITH YOUR TWITTER USERNAME


    # get list of usernames
    username_list = df['username'].values.tolist()

    # to log
    counter = 0
    for name in username_list:
        try:
            rship = client.get_friendship(source_screen_name=MY_ACCOUNT_NAME, target_screen_name=name)
            can_dm_list.append(rship[0].can_dm)
        except:
            can_dm_list.append(np.nan)
        counter += 1
        print(counter)

    # make into dataframe/table
    df["can_dm"] = can_dm_list

    # save collected data
    df.to_csv("solution_excelsheet.csv", index=False)
    
    return df


if __name__ == '__main__':
    df = main()
    
    # data report
    print("missing ", df['can_dm'].isna().sum())
    print(df['can_dm'].value_counts())