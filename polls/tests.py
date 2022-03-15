import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question, Choice

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days = days)
    return Question.objects.create(question_text = question_text, pub_date = time)

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        the detail view of a question with a pub date in the future
        returns 404 not found
        """
        future_question = create_question(question_text = "future", days = 30)
        response = self.client.get(reverse('polls:detail', args = (future_question.id, )))
        self.assertEqual(response.status_code, 404)
    def test_past_question(self):
        """
        The detail view of a question with a pub date in the past
        will show the choices and a vote button
        """
        past_question = create_question(question_text = "past", days = -30)
        response = self.client.get(reverse('polls:detail', args = (past_question.id, )))
        self.assertContains(response, past_question.question_text)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        if no questions exist, an appropriate message is displayed
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_questions(self):
        """
        questions with a pub date in the past are displayed on the index page
        """
        question = create_question(question_text = "past", days = -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question]
        )

    def test_future_questions(self):
        """
        Questions with a pub date in the future aren't displayed in the index page
        """
        question = create_question(question_text = "future", days = 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            []
        )

    def test_future_and_past_questions(self):
        """
        Even if both past and future questions exist, only past questions are displayed
        """
        future_question = create_question(question_text = "future", days = 30)
        past_question = create_question(question_text = "past", days = -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question]
        )

    def two_past_questions(self):
        """
        The question index page may display multiple questions.
        """
        q1 = create_question(question_text = "past1", days = -15)
        q2 = create_question(question_text = "past2", days = -1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [q2, q1]
        )

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days = 30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        if test was published recently (within 24 hours, it should return true)
        """
        time = timezone.now() - datetime.timedelta(hours = 23, minutes = 59, seconds = 59)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)
