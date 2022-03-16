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
        year = now.year
        month = now.month
        return reverse('birthday_tracker:detail', args = [year, month, day, ])
    def formatday(self, day, weekday):
        now = timezone.now()
        year = now.year
        month = now.month
        have_birthday_list = Person.objects.filter(birthdate__day = day, birthdate__month = month)
        if day == 0:
            return '<td id = "date" class="noday">&nbsp;</td>' # day outside month
        else:
            x = "" if len(have_birthday_list) == 0 else ' style = "color:red;" '
            return '<td id = "date" class="%s"><a %s href=' % (self.cssclasses[weekday], x) + self.detailUrl(day) + '>%d</a></td>' % (day)

def month_detail(request, year, month):
    month_name = datetime(1900, month, 1).strftime("%B")

    cal = ClickableCalendar().formatmonth(year, month)

    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    warning_message = ""
    if month != timezone.now().month:
        warning_message = "The hyperlink still doesn't work :( (This is a demo version)"

    return render(request,
        'birthday_tracker/month_calendar.html', {
        'warning_message': warning_message,
        'year': year,
        'month': month,
        'month_name': month_name,
        'month_list': month_list,
        'cal': cal,
    })

def index(request):
    now = timezone.now()
    return month_detail(request, now.year, now.month)

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
