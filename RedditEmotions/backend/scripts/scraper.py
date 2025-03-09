import prawcore.exceptions
import sklearn
import praw
import re
import os
from subreddits import *
global post_limit
post_limit = 50
global user_limit
user_limit = 100

def createAgent(clientID, clientSecret):
    reddit = praw.Reddit(
        client_id=clientID,
        client_secret=clientSecret,
        user_agent="USERAGENT",
    )
    return reddit


def extractUserData(reddit, username):
    data = " "
    try:
        current_redditor = reddit.redditor(username)
    except prawcore.exceptions.NotFound:
        return -1

    try:
        if current_redditor.is_suspended:
            return -1

    except:
        pass
    print("Username: ", username)

    submissions = current_redditor.submissions.new(limit = post_limit)
    for submission in submissions:
        if (submission.is_self and "[View Poll]" not in submission.selftext.strip()
                and "[removed]" not in submission.selftext.strip()
                and "https://preview.redd.it" not in submission.selftext.strip()):
            data += submission.selftext.strip()
            data = data.replace("\t", "")
            data = data.replace("N/A", "Not Applicable.")
            if len(submission.selftext) > 0 and submission.selftext[-1] != ".":
                data += ". "

    data += "\t"

    # print(data)
    return data.strip()

def extractSubUsers(reddit, subreddit_name, sub_data):
    users = []
    subreddit = reddit.subreddit(subreddit_name)
    if sub_data.filters == Sort.TOP:
        posts = subreddit.top(sub_data.time, limit=user_limit*5)
    else:
        posts = subreddit.new(limit=user_limit*5)
    # get the author of each post.
    for submission in posts:
        if submission.author is not None and len(users) < user_limit:
            if (submission.link_flair_text in sub_data.flair) or sub_data.flair == ["null"]:
                users.append(submission.author.name)



    return users

def extractPostCommentData(reddit, subreddit_name):
    data = " "
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.top("all", limit = post_limit/25)

    # get the comments for each post
    for submission in posts:
        for i in range(0,50):
            if data[len(data)-1] == ".":
                data = data + " "
            data = data + submission.comments[i].body
            if submission.comments[i].body[len(submission.comments[i].body)-1] != ".":
                data = data + ". "
            data = data + "\t \n"

    data = data.strip()
    return data

def saveData(body_data, name, submission_type):
    body_data = body_data.encode("utf-8", "ignore").decode("utf-8")
    body_data = body_data.replace("\t", "")
    body_data = body_data.replace("\n", "")
    body_data = re.sub(r'\s+', ' ', body_data)

    body_data += "\n    "
    f = open(submission_type + "/" + name + ".csv", "a", encoding="utf-8")
    f.writelines(body_data)
    f.close()

# reset the files
def clearFile(submission_type, name):
    f = open(submission_type + "/" + name + ".csv", "w", encoding="utf-8")
    f.close()


#Running this will update all the data stored in the files
def updateSubredditData(clientID, secretID, name):
    reddit_instance = createAgent(clientID, secretID)
    print("Updating\n", name)
    path = "../positive_samples"
    if name == "casualconversation":
        path = "../negative_samples"
    sub_data = createSub(name)
    name = os.path.splitext(name)[0]
    users = extractSubUsers(reddit_instance, name, sub_data)
    print("SUBREDDIT\n", name)
    clearFile(path, name)
    for user in users:
        data = extractUserData(reddit_instance, user)
        if data != -1:
            saveData(data, name, path)


def updateUserData(clientID, secretID):
    # for every file in '/user', run extractUserData()
    reddit_instance = createAgent(clientID, secretID)
    for name in os.listdir("../user"):
        name = os.path.splitext(name)[0]
        submission_type = "user"
        clearFile(submission_type, name)
        data = extractUserData(reddit_instance, name)
        saveData(data, name, submission_type="user")


def main(name, clientID, secretID, submission_type):
    # Create directories if they don't exist
    if not os.path.exists(submission_type):
        os.makedirs(submission_type)

    reddit_instance = createAgent(clientID, secretID)
    if not os.path.isfile(submission_type + "/" + name + ".txt"):
        if submission_type == "user":
            data = extractUserData(reddit_instance, name)
            f = open(submission_type + "/" + name + ".txt", "w", encoding="utf-8")
            f.write(data)
            f.close()

        else:
            sub_data = createSub(name)
            users = extractSubUsers(reddit_instance, name, sub_data)
            for user in users:
                data = extractUserData(reddit_instance, user)
                if data != -1:
                    saveData(data, name, submission_type)

        return data
    return -1

