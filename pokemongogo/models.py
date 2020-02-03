from django.db import models

# Create your models here.
class CounterInfo(models.Model):
    cName = models.CharField(unique=True, null=False, max_length=255)
    cCategory = models.CharField(max_length=255)
    cUrl = models.URLField(unique=True)

    def __str__(self):
        return self.cName

class News(models.Model):
    cName = models.CharField(unique=True, null=False, max_length=255)
    cDate = models.CharField(max_length=255)
    cUrl = models.URLField()

    def __str__(self):
        return self.cName

class PttArticles(models.Model):
    cName = models.CharField(unique=True, null=False, max_length=255)
    cDate = models.CharField(max_length=255)
    cUrl = models.URLField()

    def __str__(self):
        return self.cName
