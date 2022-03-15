from django.db import models
from django.utils import timezone

def givesuffix(date):
    return str(date) + "th" if 4 <= date <= 20 or 24 <= date <= 30 else ["st", "nd", "rd"][date % 10 - 1]

class Post(models.Model):
    title = models.CharField(max_length = 150)
    pub_date = models.DateTimeField('date published')
    content = models.TextField(max_length = 100000, default = "")
    upvotes = models.IntegerField(default = 0)
    def __str__(self):
        return self.title
    @property
    def get_first_sentence(self):
        return self.content.partition('.')[0] + '.'
    @property
    def get_formatted_date(self):
        return givesuffix(self.pub_date.day) + " of " + self.pub_date.strftime("%B, %H:%M:%S")

class Upvoter(models.Model):
    username = models.CharField(max_length = 150)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    def __str__(self):
        return "Upvote by " + self.username

class Comment(models.Model):
    user = models.CharField(max_length = 150, default = "")
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    content = models.TextField(max_length = 100000, default = "")
    pub_date = models.DateTimeField('date published', default = timezone.now)
    def __str__(self):
        return "Comment by " + self.user
    @property
    def get_formatted_date(self):
        return givesuffix(self.pub_date.day) + " of " + self.pub_date.strftime("%B, %H:%M:%S")