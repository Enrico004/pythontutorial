import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


# Create your tests here.

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_past_question(self):
        time = timezone.now()
        future_question = Question(pub_date=time)
        self.assertTrue(future_question.was_published_recently())
