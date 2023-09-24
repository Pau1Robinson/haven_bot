from mongoengine import *

class Playerlist(Document):
    channel_id = IntField()
    server = StringField()
    user = StringField()

class Player(Document):
    char_name = StringField()
    funcom_id = StringField()
    server_id = StringField()
    platform_id = StringField()
    platform_name = StringField()