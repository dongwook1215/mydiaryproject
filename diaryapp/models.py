from django.db import models

# Create your models here.


class Diary(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    body = models.TextField()
    page_number = models.IntegerField()

    def __str__(self):
        return self.title

    def sum(self):
        return self.body[:60]
