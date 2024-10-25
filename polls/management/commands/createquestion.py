from django.core.management.base import BaseCommand
from django.utils import timezone
import csv

from polls.models import Question, Choice


class Command(BaseCommand):
    help = 'Create random questions'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        for question in Question.objects.all():
            question.delete()
        if Question.objects.all().count() != 0:
            self.stdout.write(self.style.SUCCESS('Questions could not be created as there are some questions already existing'))
            return
        with open("polls/random_questions.csv", newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for row in reader:
                question=Question(question_text=row[0],pub_date=timezone.now())
                question.save()
                for i in range(1,5):
                    choice=Choice(question=question,choice_text=row[i],votes=0)
                    choice.save()
        self.stdout.write(self.style.SUCCESS('Questions created successfully'))