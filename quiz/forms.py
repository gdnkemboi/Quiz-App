from django import forms
from .models import Subcategory, Question, Choice


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ["category", "name"]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text"]

        labels = {
            'text': 'Question',  # Change the label for the 'text' field to 'Question'
        }

        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ["text", "is_correct"]

ChoiceFormSet = forms.inlineformset_factory(
    Question,  # Parent model
    Choice,  # Child model
    form=ChoiceForm,
    extra=2,  # Number of extra choice fields (including the first choice)
    min_num=2,  # Minimum number of choices required (including the first choice)
    validate_min=True,
    can_delete=False,  # Users cannot delete choices
)