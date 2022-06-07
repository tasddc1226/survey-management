from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import Http404
from django.urls import reverse

from ..models import Survey, Question, Choice, Submission
from ..forms import SurveyCreateForm, QuestionCreateForm, ChoiceCreateForm


@login_required
def survey_list(request):
    objs = (
        Survey.objects.filter(author=request.user).order_by("-created_at").all()
    )
    return render(request, "survey/list.html", {"surveys": objs})


@login_required
def detail(request, pk):
    try:
        survey = Survey.objects.prefetch_related(
            "question_set__choice_set"
        ).get(pk=pk, author=request.user, is_active=True)
    except Survey.DoesNotExist:
        raise Http404()

    questions = survey.question_set.all()
    # TODO: Add Calculate results

    host = request.get_host()
    public_path = reverse("survey-start", args=[pk])
    public_url = f"{request.scheme}://{host}{public_path}"
    num_submissions = survey.submission_set.filter(is_complete=True).count()
    return render(
        request,
        "survey/detail.html",
        {
            "survey": survey,
            "public_url": public_url,
            "questions": questions,
            "num_submissions": num_submissions,
        },
    )


@login_required
def create(request):
    if request.method == "POST":
        form = SurveyCreateForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.author = request.user
            survey.save()
            return redirect("survey-edit", pk=survey.id)
    else:
        form = SurveyCreateForm()
    return render(request, "survey/create.html", {"form": form})


@login_required
def delete(request, pk):
    survey = get_object_or_404(Survey, pk=pk, author=request.user)
    if request.method == "POST":
        survey.delete()

    return redirect("survey-list")


@login_required
def edit(request, pk):
    try:
        survey = Survey.objects.prefetch_related(
            "question_set__choice_set"
        ).get(pk=pk, author=request.user, is_active=False)
    except Survey.DoesNotExist:
        raise Http404()

    if request.method == "POST":
        survey.is_active = True
        survey.save()
        return redirect("survey-detail", pk=pk)
    else:
        questions = survey.question_set.all()
        return render(
            request,
            "survey/edit.html",
            {"survey": survey, "questions": questions},
        )


@login_required
def question_create(request, pk):
    survey = get_object_or_404(Survey, pk=pk, author=request.user)
    if request.method == "POST":
        form = QuestionCreateForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.save()
            return redirect(
                "survey-choice-create", survey_pk=pk, question_pk=question.pk
            )
    else:
        form = QuestionCreateForm()

    return render(
        request, "survey/question.html", {"survey": survey, "form": form}
    )


@login_required
def question_delete(request, survey_pk, question_pk):
    survey = get_object_or_404(Survey, pk=survey_pk, author=request.user)
    question = Question.objects.get(pk=question_pk)
    if request.method == "POST":
        question.delete()

    return redirect("survey-edit", pk=survey_pk)


@login_required
def choice_create(request, survey_pk, question_pk):
    survey = get_object_or_404(Survey, pk=survey_pk, author=request.user)
    question = Question.objects.get(pk=question_pk)
    if request.method == "POST":
        form = ChoiceCreateForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question_id = question_pk
            choice.save()
    else:
        form = ChoiceCreateForm()
    choices = question.choice_set.all()
    return render(
        request,
        "survey/choices.html",
        {
            "survey": survey,
            "question": question,
            "choices": choices,
            "form": form,
        },
    )


def start(request, pk):
    survey = get_object_or_404(Survey, pk=pk, is_active=True)
    if request.method == "POST":
        sub = Submission.objects.create(survey=survey)
        return redirect("survey-submit", survey_pk=pk, sub_pk=sub.pk)

    return render(request, "survey/start.html", {"survey": survey})