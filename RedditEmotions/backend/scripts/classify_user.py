import pickle as pk


def loadUser(username):
    f = open("user/" + username + ".txt", "r", encoding="utf-8")
    data = f.read()
    f.close()
    return data

def loadSubredditModel(sub_name):
    return pk.load(open("models/" + sub_name + ".sav", 'rb'))

def classifyWithModel(model, user_data, subreddit_name):

    user_data = user_data.replace("\t", "")

    vectorizer = pk.load(open("vectorizers/" + subreddit_name + "vectorizer.pk", 'rb'))
    user_data_transformed = vectorizer.transform([user_data])
    predicted_sentiment = model.predict_proba(user_data_transformed)
    return predicted_sentiment[0]



def main(subreddit_name, username):
    user = loadUser(username)
    model = loadSubredditModel(subreddit_name)
    if user != "":
        fin = classifyWithModel(model, user, subreddit_name)
        return fin[1]
    else:
        return -1

# main("depression", "username")