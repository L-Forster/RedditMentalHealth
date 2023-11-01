import classify_user

def main(subreddit_name, user):
    return classify_user.main(subreddit_name, user)

def classify_raw(subreddit_name, data):
    model = classify_user.loadSubredditModel(subreddit_name)
    return classify_user.classifyWithModel(model, data, subreddit_name)


# print(classify_raw("narcissism", "I am the greatest person alive. No-one even gets close to me!"))
