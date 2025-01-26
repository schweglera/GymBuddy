# Create your views here.
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from django.forms import modelformset_factory
from .forms import ArticleForm, TrainingPlanCreateForm, MealPlanCreateForm
from .forms import WorkoutCreateForm
from .forms import ExerciseCreateForm
from .forms import CommentForm
from .forms import AdminRegisterForm
from .forms import CoachCreateForm
from .models import Article, TrainingPlan, Workout, Exercise, MealPlan, Coach

ExerciseCreateFormSet = modelformset_factory(Exercise, form=ExerciseCreateForm, extra=1)



def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == "POST":
        # Erstelle ein Formular mit den Daten, die der Benutzer gesendet hat
        form = CommentForm(request.POST)

        if form.is_valid():
            # Erstelle eine Comment-Instanz aus den Formular-Daten; speichere sie
            # jedoch noch nicht in der DB ab, da wir den Kommentar mit dem Artikel verlinken
            # müssen (via Fremdschlüsselbeziehung).
            comment = form.save(commit=False)
            # Verlinke den Kommentar mit dem Artikel
            comment.article = article
            comment.save()
            return redirect("article_detail", pk=article.pk)
    else:
        # Erstelle ein neues Formular zur Anzeige
        form = CommentForm()

    # Im Falle eines GET-Requests: Formular wird gerendert (via "form" Feld)
    return render(request, "article_detail.html", {"article": article, "form": form})


def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            return redirect("article_detail", pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, "add_article.html", {"form": form})




#------------------------

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

def community(request):
    # [2]
    articles = Article.objects.all().order_by('-id')
    return render(request, "all_community.html", {"articles": articles})

@login_required
def workout_list(request):
    workouts = Workout.objects.filter(user=request.user)
    return render(request, "workout_list.html", {"workouts": workouts})



from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def adminregister(request):
    if request.method == "POST":
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = AdminRegisterForm()
    return render(request, "adminregister.html", {"form": form})


@login_required
def dashboard(request):
    user = request.user
    workouts = user.workout_set.all().order_by('-date')[:5]
    mplans = user.mealplan_set.all()
    tplans = user.trainingplan_set.all()

    return render(request, "user/dashboard.html", {
        "workouts": workouts,
        "mplans": mplans,
        "tplans": tplans,
    })

@login_required
def all_workouts(request):
    user = request.user
    workouts = user.workout_set.all().order_by('-date')
    return render(request, "user/all_workouts.html", {"workouts": workouts})

def homepage(request):
    articles = Article.objects.all().order_by('-id')[:5]
    is_admin = request.user.is_authenticated and request.user.groups.filter(name="Admin").exists()

    return render(request, "homepage.html", {"articles": articles, "is_admin": is_admin})



@login_required
def workout_create(request):
    if request.method == "POST":
        workout_form = WorkoutCreateForm(request.POST)
        exercise_formset = ExerciseCreateFormSet(request.POST, queryset=Exercise.objects.none())

        if workout_form.is_valid() and exercise_formset.is_valid():
            workout = workout_form.save(commit=False)
            workout.user = request.user
            workout.save()

            for exercise_form in exercise_formset:
                if exercise_form.cleaned_data:
                    exercise = exercise_form.save(commit=False)
                    exercise.workout = workout
                    exercise.save()

            return redirect("dashboard")
    else:
        workout_form = WorkoutCreateForm()
        exercise_formset = ExerciseCreateFormSet(queryset=Exercise.objects.none())

    return render(request, "workout_create.html", {
        "workout_form": workout_form,
        "exercise_formset": exercise_formset,
    })

@login_required
def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    exercises = workout.exercises.all()
    return render(request, "workout_detail.html", {
        "workout": workout,
        "exercises": exercises,
    })

@login_required
def tplan(request):
    user = request.user
    tplans = user.trainingplan_set.all().order_by('name')
    return render(request, "user/all_tplan.html", {"tplans": tplans})


@login_required
def tplan_create(request):
    if request.method == "POST":
        form = TrainingPlanCreateForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            return redirect("dashboard")
    else:
        form = TrainingPlanCreateForm()

    return render(request, "tplan_create.html", {"form": form})

@login_required
def tplan_detail(request, pk):
    tplan = get_object_or_404(TrainingPlan, pk=pk, user=request.user)
    return render(request, "user/tplan_detail.html", {"tplan": tplan})


@login_required
def mplan(request):
    user = request.user
    mplans = user.mealplan_set.all().order_by('name')
    return render(request, "user/all_mplan.html", {"mplans": mplans})


@login_required
def mplan_create(request):
    if request.method == "POST":
        form = MealPlanCreateForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            return redirect("dashboard")
    else:
        form = MealPlanCreateForm()

    return render(request, "mplan_create.html", {"form": form})

@login_required
def mplan_detail(request, pk):
    mplan = get_object_or_404(MealPlan, pk=pk, user=request.user)
    return render(request, "user/mplan_detail.html", {"mplan": mplan})


def is_admin(user):
    return user.is_authenticated and user.groups.filter(name="Admin").exists()

@user_passes_test(is_admin)
def coach_create(request):
    if request.method == "POST":
        form = CoachCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("homepage")

    else:
        form = CoachCreateForm()

    return render(request, "coach_create.html", {"form": form})

def coach(request):
    coaches = Coach.objects.all()
    return render(request, "all_coach.html", {"coaches": coaches})

def coach_detail(request, pk):
    coach = get_object_or_404(Coach, pk=pk)
    return render(request, "coach_detail.html", {"coach": coach})

