from mongoengine import Document, StringField, ListField

class Link(Document):
  Link = StringField(required=True, max_length=200)

class Post(Document):
  Title = StringField(required=True)
  RelatedTo = ListField(required=True)


class Submission(Document):
    link = StringField(required=True)
    tags = ListField(StringField(max_length=30))


class User(Document):
    name = StringField(required=True)
    link = StringField(required=True)
    tags = ListField(StringField(max_length=30))
    email = StringField(required=True)