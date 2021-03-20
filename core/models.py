from mongoengine import (Document, QuerySetManager, StringField,
                         ListField, BooleanField, DateTimeField, DecimalField)
from datetime import datetime


class UserModel(Document):
    objects = QuerySetManager()
    meta = {'collection': 'user'}

    user_name = StringField(required=True, unique=True)
    password = StringField(required=True)
    email = StringField(unique=True)
    roles = ListField(StringField(default='user'))

    name = StringField()
    active = BooleanField(required=True, default=True)
    time_created = DateTimeField(default=datetime.utcnow())

    @classmethod
    def find_all(cls):
        return cls.objects()

    @classmethod
    def find_by_username(cls, name):
        try:
            user = cls.objects.get(user_name=name)
        except Exception:
            return None

        return user

    @classmethod
    def find_by_email(cls, email):
        try:
            user = cls.objects.get(email=email)
        except Exception:
            return None

        return user


class NotificationModel(Document):
    objects = QuerySetManager()
    meta = {'collection': 'notification'}

    timestamp = DateTimeField(default=datetime.utcnow())
    notification_type = StringField(required=True)
    description = StringField()
    probability = DecimalField()
    confidence = DecimalField()
    impact_expect = DecimalField()
    external_url = StringField()
    notification_list = StringField(required=True)

    @classmethod
    def find_all(cls):
        return cls.objects()

    @classmethod
    def find_by_time(cls, limit):

        try:
            notification = cls.objects(timestamp__lte=limit)
        except Exception:
            return None

        return notification
    
    @classmethod
    def find_by_notification_list(cls, list):
        notifications = cls.objects(notification_list=list)
        if not notifications:
            return None 
        return notifications


class NotificationListModel(Document):
    object = QuerySetManager()
    meta = {'collection': 'notification_list'}

    name = StringField(required=True, unique=True)
    last_changed = DateTimeField(default=datetime.utcnow())

    @classmethod
    def find_all(cls): 
        return cls.objects()

    @classmethod
    def find_by_name(cls, name):
        notification_list= cls.objects(name=name)
        if not notification_list:
           return None
        return notification_list
