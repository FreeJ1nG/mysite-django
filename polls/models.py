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
    def get_top_3_votes(self):
        return self.choice_set.order_by('-votes')[0:3]
    def get_total_votes(self):
        return sum([choice.votes for choice in self.choice_set.all()])
    def get_formatted_date(self):
        def givesuffix(date):
            return str(date) + "th" if 4 <= date <= 20 or 24 <= date <= 30 else ["st", "nd", "rd"][date % 10 - 1]
        return givesuffix(self.pub_date.day) + " of " + self.pub_date.strftime("%B, %H:%M:%S")
    def get_highest_vote(self):
        return self.choice_set.order_by('-votes')[0]
    def get_sorted_by_vote(self):
        return self.choice_set.order_by('-votes')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
