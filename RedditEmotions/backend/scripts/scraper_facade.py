import scraper

def main(name, type):
    clientID = "CLIENT KEY HERE"
    secretID = "SECRET KEY HERE"

    if type == "update":
        scraper.updateSubredditData(clientID, secretID, name)
    else:
        scraper.main(name, clientID, secretID, type)



# main(name, type)
# main("npd","update")
# main("casualconversation","update")
# main("bipolar", "update")