from Scraper import *
import time
from config_loader import Config

# PRAW constants


# Twilio constants



def notify(notifier, post, message):
    if notifier.checkIfAlreadySent(post):
        notifier.sendMessage('8042100901','17572092974', message)
        notifier.addToExemptionList(post)


def main():
    # initialize core objects
    scraper = Scraper(Config.praw('CLIENT_ID'), Config.praw('CLIENT_SECRET'), Config.praw('USER_AGENT'), Config.praw('USERNAME'), Config.praw('PASSWORD'))
    parser = Parser()
    notifier = Notifier(Config.twilio('ACCOUNT_SID'), Config.twilio('AUTH_TOKEN'))

    # initialize time for loop
    startTime = time.time()

    while True:
        try:
            # grab last 100 new mechmarket posts
            posts = scraper.grabNewPosts('mechmarket', 100)

            # loop through posts
            for post in posts:
                have = parser.parseHave(post.title)
                # does this need the or? or is the search case insensitive?
                if parser.keywordSearch('milkshake', have) or parser.keywordSearch('Milkshake', have):
                    # notify if we found it
                    notify(notifier, post,
                           f'Milkshake found '\
                           f'{post.title} '\
                           f'{post.url} ')
            # sleep for 60 seconds
            time.sleep(60.0 - ((time.time() - startTime) % 60.0))
            print(f'Starting new loop at {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')
        except:
            # disable during testing
            # notifier.sendMessage('8042100901','17572092974','Something broke and the bot has stopped')
            break

main()
