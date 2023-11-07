import os
from RedditEmotions.scripts import classify_facade, scraper_facade, training_facade


def main(subreddit, user, type):

    # Create the Model from the subreddit, if there is not already one.
    stored_subreddits = os.listdir("positive_samples")
    file = subreddit + ".csv"
    if file not in stored_subreddits or type == "update":
        scraper_facade.main(subreddit, type)

    file = subreddit + ".sav"
    if file not in os.listdir("models") or type == "update":
        training_facade.main(subreddit, "positive_samples")

    if type == "raw":
        prob = classify_facade.classify_raw(subreddit, user)
        return prob[1]
    elif type != "update":
        scraper_facade.main(user, type)

        # Run the model with the user's data
        prob = classify_facade.main(subreddit, user)
        print(prob)
        return prob

    return 0


# main("bipolar", "", "update")
