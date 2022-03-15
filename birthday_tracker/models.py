from django.db import models
from django.utils import timezone
from datetime import datetime

def givesuffix(date):
    return str(date) + "th" if 4 <= date <= 20 or 24 <= date <= 30 else ["st", "nd", "rd"][date % 10 - 1]

class Person(models.Model):
    name = models.CharField(max_length = 50)
    instagram = models.CharField(max_length = 20)
    birthdate = models.DateTimeField(default = datetime(1500, 1, 1, 12, 0, 0, 0))
    def __str__(self):
        str_representation = self.name + " is having his/her birthday on the " + givesuffix(self.birthdate.day) + " of " + self.birthdate.strftime("%B") + "."
        return str_representation
    def is_today_birthday(self):
        now = timezone.now()
        return now.month == self.birthdate.month and now.day == self.birthdate.day
