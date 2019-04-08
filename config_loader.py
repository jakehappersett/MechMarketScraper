# config_loader.py
from configparser import ConfigParser
import os


class Config:
    """Interact with configuration variables."""

    configParser = ConfigParser()
    configFilePath = (os.path.join(os.getcwd(), 'config.ini'))

    @classmethod
    def initialize(cls, newhire_table):
        """Start config by reading config.ini."""
        cls.configParser.read(cls.configFilePath)

    @classmethod
    def praw(cls, key):
        """Get PRAW values from config.ini."""
        return cls.configParser.get('PRAW', key)

    @classmethod
    def twilio(cls, key):
        """Get Twilio values from config.ini."""
        return cls.configParser.get('TWILIO', key)