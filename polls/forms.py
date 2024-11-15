from django import forms

from polls.models import Choice


class VoteForm(forms.Form):
    # creating the form for voting filling it with the choices,
    # default empty choices, empty choice not displayed
    choice = forms.ModelChoiceField(queryset=Choice.objects.none(), empty_label=None)

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question') # pop the question from the kwargs
        super().__init__(*args, **kwargs)
        self.fields['choice'].queryset = question.choice_set.all() # add it to the field container

# Explanation
# ModelChoiceField: allows users to select from a list of choices related to the Choice model
# Dynamic Queryset: the queryset for the choice field is initially set to the Choice.objects.none(), meaning it has no
# In the __init__ method, the form takes an additional question argument
# This argument is used to filter the choices related to the specific question, ensuring that only relevant choices are displayed
# self.fields is an attribute of Django forms that holds a dictionary of form fields.
# Each key in the dictionary is the name of field, and the corresponding value is an instance of a form
# field class (e.g. CharField, ModelChoiceField)
# This attribute allows you to dynamically access and modify the form fields with the form class
# This ensures that users can only vote for choices associated with the current question