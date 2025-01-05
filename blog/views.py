# Create your views here.
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import ArticleForm
from .forms import CommentForm
from .models import Article





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

@login_required
def dashboard(request):
    user = request.user
    workouts = user.workout_set.all().order_by('-date')[:5]  # Zeigt die letzten 5 Workouts
    meal_plans = user.mealplan_set.all()
    training_plans = user.trainingplan_set.all()

    return render(request, "user/dashboard.html", {
        "workouts": workouts,
        "meal_plans": meal_plans,
        "training_plans": training_plans,
    })

@login_required
def all_workouts(request):
    user = request.user
    workouts = user.workout_set.all().order_by('-date')  # Alle Workouts des eingeloggten Benutzers
    return render(request, "user/all_workouts.html", {"workouts": workouts})

def article_list(request):
    articles = Article.objects.all()[:5]  # Letzte 5 Artikel
    return render(request, "article_list.html", {"articles": articles})




@login_required
def workout_create(request):
    # Workout-Recorder wird hier später implementiert
    return render(request, "workout_create.html", {})

@login_required
def coach_shop(request):
    # Coach-Shop wird hier später implementiert
    return render(request, "coach_shop.html", {})