import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    @admin.display(
        boolean = True,
        ordering = 'pub_date',
        description = 'Published recently?',
    )
    def was_published_recently(self):
        cur_time = timezone.now()
        return cur_time >= self.pub_date >= cur_time - datetime.timedelta(days = 1)
    def __str__(self):
        return "The question is: " + self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
