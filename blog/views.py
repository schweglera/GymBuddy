# Create your views here.
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import ArticleForm
from .forms import CommentForm
from .models import Article


def article_list(request):
    articles = Article.objects.all()
    return render(request, "article_list.html", {"articles": articles})


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

