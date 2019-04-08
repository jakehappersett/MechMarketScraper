import praw
from twilio.rest import Client
from config_loader import Config


class Scraper:

    # add all inputs as parameters
    # add startup test (check reddit.username.me)
    def __init__(self, client_id, client_secret, user_agent, username, password):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.username = username
        self.password = password
        self.client = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
            username=self.username,
            password=self.password)

    def grabNewPosts(self, sub, lim):
        """
        Grab new posts from subreddit
        :param sub: subreddit name, string
        :param lim: number of posts to return, integer
        :return: list of posts
        """
        return [submission for submission in self.client.subreddit(sub).new(limit=lim)]


class Parser:

    def __init__(self):
        self.h = '[H]'
        self.w = '[W]'

    def parseHave(self, title):
        # takes in a post title returns list of objects after [H] and before [W]
        return title[title.find(self.h)+3: title.find(self.w)].split()

    def parseWant(self, title):
        # takes in a post title and returns list of objects after [W] and before [H]
        return title[title.find(self.w)+3:].split()

    def keywordSearch(self, searchTerm, values):
        """
        takes in list of keyboards and a value we are searching for
        return true if keyword is found
        :type title: list
        """
        for val in values:
            if searchTerm in val:
                return True


class Notifier:

    def __init__(self, accountSID, authToken):
        """
        send a text message via twilio when we find the keyset
        todo : add startup test
        :param accountSID:
        :param authToken:
        """
        self.accountSID = accountSID
        self.authToken = authToken
        self.client = Client(self.accountSID, self.authToken)
        self.ex = self.initializeExemptionList()

    def initializeExemptionList(self):
        """
        check to see if the exemption list exists create it if not
        :return:
        """
        try:
            ex = open("exceptionList.txt", "r")
        except FileNotFoundError:
            ex = open("exceptionList.txt", "w")
        ex.close()
        return ex

    def checkIfAlreadySent(self, post):
        """
        return True if post has not been sent
        :param post: reddit post
        """
        file = open(self.ex.name, "r")
        for line in file:
            line = line.rstrip()
            if post.title == line:
                return False
        return True

    def addToExemptionList(self, post):
        """
        add post to sent list
        :param post: reddit post
        """
        file = open(self.ex.name, "a")
        file.write(post.title + '\n')
        file.close()

    def sendMessage(self, messageTo, messageFrom, messageBody):
        message = self.client.messages.create(to=messageTo, from_=messageFrom, body=messageBody)
        return message
