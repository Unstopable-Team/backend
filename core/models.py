from mongoengine import Document, QuerySetManager, StringField, ListField, BooleanField, DateTimeField, DecimalField
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
