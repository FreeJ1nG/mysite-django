from django.template import loader
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import *

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:10]
    choice_list = []
    for question in latest_question_list:
        choice_list.append(Question.objects.get(id = question.id).choice_set.order_by('votes')[:3])
    return render(request, 'polls/index.html', {
        'latest_question_list': latest_question_list,
        'choice_list': choice_list,
    })

def detail(request, poll_id):
    question = get_object_or_404(Question, id = poll_id)
    return render(request, 'polls/detail.html', {'question' : question})

def results(request, poll_id):
    question = get_object_or_404(Question, id = poll_id)
    return render(request, 'polls/results.html', {'question' : question})

def vote(request, poll_id):
    question = get_object_or_404(Question, id = poll_id)
    try:
        selected_choice = question.choice_set.get(id = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question' : question,
            'error_message' : 'You did not select a choice',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args = (question.id, )))
