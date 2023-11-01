import os
import pickle as pk
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

#train data based on specific subreddits and behaviours

#Input data Sets:

## Positive ##
# Depression positive_samples/depression: https://www.reddit.com/r/depression/
# Anxiety positive_samples/anxiety: https://www.reddit.com/r/Anxiety/?f=flair_name%3A%22Therapy%22
# ADHD positive_samples/adhd https://www.reddit.com/r/ADHD/?f=flair_name%3A%22Seeking%20Empathy%22
# Schizophrenia: https://www.reddit.com/r/schizophrenia/?f=flair_name%3A%22Seeking%20Support%22
# https://www.reddit.com/r/schizophrenia/?f=flair_name%3A%22Rant%20%2F%20Vent%22
# Bipolar https://www.reddit.com/r/bipolar/?f=flair_name%3A%22Support%2FAdvice%20%3Ashy%3A%22 https://www.reddit.com/r/bipolar/?f=flair_name%3A%22Discussion%20%3Anervous%3A%22
# Narcissism: https://www.reddit.com/r/NPD/ https://www.reddit.com/r/narcissism/
# Autism: https://www.reddit.com/r/autism/?f=flair_name%3A%22Rant%2FVent%22, https://www.reddit.com/r/autism/?f=flair_name%3A%22Discussion%22, https://www.reddit.com/r/autism/?f=flair_name%3A%22Question%22, https://www.reddit.com/r/autism/?f=flair_name%3A%22Advice%22
# Paranoia /// Too similar to anxiety.
# Antisocial personality disorder: https://www.reddit.com/r/aspd/?f=flair_name%3A%22Rant%22 TAKE COMMENTS:{ https://www.reddit.com/r/aspd/?f=flair_name%3A%22Discussion%22 T  ... https://www.reddit.com/r/aspd/?f=flair_name%3A%22Advice%20%22}

####################





def trainOnSub(subreddit, path):


    df_neg = pd.read_csv("negative_samples/casualconversation.csv", header=None, sep="\t")
    df_pos = pd.read_csv("positive_samples/" +subreddit + ".csv", header=None, sep="\t")


    df_pos["sentiment"] = 1
    df_neg["sentiment"] = 0
    df = pd.concat([df_pos, df_neg])
    x = df[0]
    y = df["sentiment"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)


    vectorizer = TfidfVectorizer(sublinear_tf=True, encoding='utf-8',
                             decode_error='ignore')
    x_train = vectorizer.fit_transform(x_train)
    x_test = vectorizer.transform(x_test)

    # train
    model = SVC(probability=True)
    model.fit(x_train, y_train)

    #  predictions
    y_pred = model.predict(x_test)

    # accuracy
    model_accuracy = accuracy_score(y_test, y_pred)


    print("Accuracy:", accuracy_score(y_test, y_pred))


    return model, model_accuracy, vectorizer


def saveModel(model, subreddit, vectorizer):
    with open("models" + "/" + subreddit + ".sav", 'wb') as f:
        pk.dump(model, f)
    pk.dump(vectorizer, open("vectorizers/" + subreddit + "vectorizer.pk", "wb"))

    print("Model Updated! \n")

def generateBestModel(file, path):
    filepath = file + " acc.txt"
    if filepath not in os.listdir("accuracy_values"):
        score_f = open("accuracy_values/" +filepath, "w")
        score_f.write("0.0")
        score_f.close()

    score_f = open( "accuracy_values/"+filepath, "r")
    best_score = (score_f.read())
    if best_score == "":
        best_score = 0.0
    else:
        best_score = float(best_score)

    score_f.close()
    score_f = open( "accuracy_values/"+filepath, "w")
    for i in range(0,10):
        model,accuracy, vectorizer = trainOnSub(file, path)

        if accuracy > best_score:
            best_score = accuracy
            saveModel(model, file, vectorizer)
            print("Updating best model...")


    print(best_score)
    score_f.write(str(best_score))
    score_f.close()

def main(file, path):
    generateBestModel(file,path)

# main("aspd", "positive_samples")