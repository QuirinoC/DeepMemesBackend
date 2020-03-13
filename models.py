from mongoengine import Document, StringField, ListField

class Link(Document):
  Link = StringField(required=True, max_length=200)

class Post(Document):
  Title = StringField(required=True)
  RelatedTo = ListField(required=True)
