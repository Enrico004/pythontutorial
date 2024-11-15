from django.db.models import F
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from django.views.generic.edit import FormView

from polls.forms import VoteForm
from polls.models import Question, Choice


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


class VoteView(FormView):
    form_class = VoteForm
    template_name = "polls/details.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # get the question object from the database
        # and pass it tot the form as a keyword argument
        kwargs['question'] = get_object_or_404(Question, pk=self.kwargs['question_id'])
        return kwargs

    def form_valid(self, form):
        # cleaned data is a dictionary that contains the validated
        # and cleaned data from the form fields
        # After a form is submitted and validated, cleaned_data holds
        # the data that has passed validation checks
        # Define a clean_<fieldname> method to add custom validation
        # logic for specific field
        selected_choice = form.cleaned_data['choice']
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(selected_choice.question.id,)))

    def form_invalid(self, form):
        question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        return render(self.request, self.template_name, context={
            'question': question,
            'form': form,
            'error_message': "You didn't select a choice.",
        })

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST["choice"])
#     except (KeyError, Choice.DoesNotExist):
#         return render(request, 'polls/details.html', {"question": question, "error_message": "Please select a choice"})
#     else:
#         selected_choice.votes = F("votes") + 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#     return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
