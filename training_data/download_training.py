import praw
from psaw import PushshiftAPI
import datetime as dt

import sys
import re

import pandas as pd
import sqlite3
import datetime
import logging

import requests

# Gets age and gender from r4r style title
def get_age_gender_from_title(text):
    
    gender_re = r'(?<=\[)[A-z](?=4[A-z]\])'
    age_re = r'[0-9]* *(?=\[[A-z]4[A-z]\])'

    gender = re.search(gender_re, text).group(0)
    age = re.search(age_re, text).group(0)

    return gender, age


# Converts comments into a dictionary to be used in a pandas dataframe
def submission_to_row(submission):
    # Handles linked posts
    content = submission.selftext
    author = None
    if content == "":
        content = get_linked_content(submission.url)
    if submission.author != None:
        author = submission.author.name

    # Creates and returns dictionary
    return {
        'id': submission.id,
        'author': author,
        'title': submission.title,
        'creation_date': datetime.datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
        'content': content,
    }


# Converts a comment into row form to be put in a pandas dataframe

def comment_to_row(comment):

    author = None

    if(comment.author != None):
        author = comment.author.name

    return {
        'id': comment.id,
        'creation_date': datetime.datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
        'content': comment.body,
        'author': author,
    }


def subreddit_download_to_csv(subreddit, reddit, api, limit=None, start_date = None, end_date = None):
    
    gen = api.search_submissions(after=start_date, before=end_date, subreddit=subreddit, limit=limit)

    output = []

    for submission in gen:
        # will limit the earlies date of scraping
        try:
            submission = submission_to_row(submission)

            if submission['author'] is None:
                continue

            gender, age = get_age_gender_from_title(submission['title'])

            for comment in reddit.redditor(submission['author']).comments.new(limit=50).__iter__():
                output.append({
                    'user' : submission['author'],
                    'gender' : gender,
                    'age' : age,
                    'comment' : comment.body.replace('\n',' ').replace(',', '').replace('\t', ' '),
                    #'date' : comment.created_utc
                    })
                    
            logging.debug('Finished extracting post: "%s"', submission.title)
        except:
            logging.debug('Failed extracting post:')
            pass
    
    df = pd.DataFrame(output)
    print(df)
    df.to_csv('1_year_training.csv')


def main():
    reddit = praw.Reddit(client_id=str(sys.argv[1]),
                         client_secret=str(sys.argv[2]),
                         user_agent=str(sys.argv[3]))
    
    api = PushshiftAPI(reddit)

    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', level=logging.INFO)
    subreddit_download_to_csv('r4r', reddit, api, None, datetime.datetime(2019,11,29),datetime.datetime(2020,11,29))


if __name__ == "__main__":
    main()
