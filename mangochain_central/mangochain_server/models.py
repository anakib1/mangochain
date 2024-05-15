from django.db import models

# Create your models here.
# messages/models.py
from django.db import models


class Block(models.Model):
    content = models.TextField()


class User(models.Model):
    userName = models.TextField()
    signature = models.TextField()


class Transaction(models.Model):
    from_id = models.TextField()
    to_id = models.TextField()
    tr_id = models.TextField()
    amount = models.FloatField()
    signature = models.TextField()
