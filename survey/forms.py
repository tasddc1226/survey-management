from django import forms
from .models import Survey, Question, Choice, Submission
from django.core.exceptions import ValidationError


class SurveyCreateForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = [
            "title",
            "description",
        ]


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question_text", "answer_type"]


class ChoiceCreateForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ["choice_text"]


class PhoneCreateForm(forms.ModelForm):
    error_messages = {"exists_phone": "Already exists phone number."}

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if Submission.objects.filter(phone=phone).exists():
            raise ValidationError(self.error_messages["exists_phone"])
        return phone

    class Meta:
        model = Submission
        fields = ["phone"]


class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop("choices")
        type = kwargs.pop("answer_types")
        lists = {(c.pk, c.choice_text) for c in choices}
        super().__init__(*args, **kwargs)

        if type == 1:
            choice_field = forms.ChoiceField(
                choices=lists, widget=forms.RadioSelect, required=True
            )
        elif type == 2:
            choice_field = forms.ChoiceField(
                choices=lists,
                widget=forms.CheckboxSelectMultiple,
                required=True,
            )
        elif type == 3:
            choice_field = forms.ChoiceField(
                choices=lists, widget=forms.Select, required=True
            )

        self.fields["choice"] = choice_field


class BaseAnswerFormSet(forms.BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["choices"] = kwargs["choices"][index]
        kwargs["answer_types"] = kwargs["answer_types"][index]
        return kwargs
