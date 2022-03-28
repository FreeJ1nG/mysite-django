from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField

def givesuffix(date):
    return str(date) + ("th" if 4 <= date <= 20 or 24 <= date <= 30 else ["st", "nd", "rd"][date % 10 - 1])

class Post(models.Model):
    title = models.CharField(max_length = 150)
    pub_date = models.DateTimeField('date published', default = timezone.now())
    content = RichTextField(blank = True, null = True)
    upvotes = models.IntegerField(default = 0)
    def __str__(self):
        return self.title
    def get_first_sentence(self):
        return self.content.partition('.')[0] + '.'
    def get_formatted_date(self):
        return givesuffix(self.pub_date.day) + " of " + self.pub_date.strftime("%B, %H:%M:%S")
    def get_comment_amount(self):
        return len(self.comment_set.all())
    def get_upvote_amount(self):
        return len(self.upvoter_set.all())
    def get_absolute_url(self):
        return reverse('blog:detail', args = (self.id, ))

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
    edited = models.BooleanField(default = False)
    def __str__(self):
        return "Comment by " + self.user
    @property
    def get_formatted_date(self):
        return givesuffix(self.pub_date.day) + " of " + self.pub_date.strftime("%B, %H:%M:%S")
