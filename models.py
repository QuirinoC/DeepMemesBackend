from mongoengine import Document, StringField

class Link(Document):
  Link = StringField(required=True, max_length=200)