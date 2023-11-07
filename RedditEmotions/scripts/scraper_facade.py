from RedditEmotions.scripts import scraper


def main(name, type):
    clientID = "INSERT CLIENT KEY"
    secretID = "INSERT SECRET KEY"

    if type == "update":
        scraper.updateSubredditData(clientID, secretID, name)
    else:
        scraper.main(name, clientID, secretID, type)



# main(name, type)
# main("npd","update")
# main("casualconversation","update")
# main("bipolar", "update")