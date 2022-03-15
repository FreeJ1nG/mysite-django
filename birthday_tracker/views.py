from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Person

class ClickableCalendar(HTMLCalendar):
    def detailUrl(self, day):
        now = timezone.now()
        month = now.month
        year = now.year
        return reverse('birthday_tracker:detail', args = [year, month, day])
    def formatday(self, day, weekday):
        now = timezone.now()
        month = now.month
        year = now.year
        have_birthday_list = Person.objects.filter(birthdate__day = day, birthdate__month = month)
        if day == 0:
            return '<td class="noday">&nbsp;</td>' # day outside month
        else:
            x = "" if len(have_birthday_list) == 0 else ' style = "color:red" '
            return '<td class="%s"><a %s href=' % (self.cssclasses[weekday], x) + self.detailUrl(day) + '>%d</a></td>' % (day)

def index(request):
    now = timezone.now()
    month = now.month
    year = now.year

    month_name = datetime(1900, month, 1).strftime("%B")

    cal = ClickableCalendar().formatmonth(year, month)

    return render(request,
        'birthday_tracker/index.html', {
        'month': month,
        'month_name': month_name,
        'year': year,
        'cal': cal,
    })

def detail(request, year, month, day):
    have_birthday_list = Person.objects.filter(birthdate__month = month, birthdate__day = day)
    no_birthday_message = "Today nobody's happy :("
    day_month_year_display_message = "Today, these are happy people! :D"
    return render(request,
        'birthday_tracker/detail.html', {
        'have_birthday_list': have_birthday_list,
        'no_birthday_message': no_birthday_message,
        'day_month_year_display_message': day_month_year_display_message,
    })

def insert_input(request):
    name = request.POST.get("name")
    instagram = request.POST.get("instagram")
    birthdate = request.POST.get("birthdate")
    birthdate = datetime.fromisoformat(birthdate)
    person = Person(name = name, instagram = instagram, birthdate = birthdate)
    person.save()
    return HttpResponseRedirect(reverse('birthday_tracker:index'))

def input(request):
    return render(request, 'birthday_tracker/input.html', {})
