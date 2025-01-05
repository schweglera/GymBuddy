from django.test import TestCase
from django.urls import reverse
from django.utils.html import escape
from ..models import Article, Comment


class ArticleListViewTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title="Test Article", content="Test content for article."
        )

    def test_article_list_view_renders_correctly(self):
        response = self.client.get(reverse("article_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blog Artikel")
        self.assertContains(response, self.article.title)

    def test_article_list_view_no_articles(self):
        Article.objects.all().delete()
        response = self.client.get(reverse("article_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blog Artikel")
        self.assertNotContains(response, self.article.title)


class ArticleDetailViewTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title="Test Article", content="Test content for article."
        )
        self.comment = Comment.objects.create(
            article=self.article, author="Tester", text="A test comment"
        )

    def test_article_detail_view_renders_correctly(self):
        response = self.client.get(reverse("article_detail", args=[self.article.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)
        self.assertContains(response, self.article.content)
        self.assertContains(response, "Kommentare")
        self.assertContains(response, escape(self.comment.text))

    def test_article_detail_view_post_comment(self):
        response = self.client.post(
            reverse("article_detail", args=[self.article.pk]),
            {"author": "Neuer Tester", "text": "Ein neuer Kommentar"},
        )
        self.assertEqual(response.status_code, 302)
        # Holt den zuletzt hinzugefügten Kommentar aus der Datenbank basierend auf der höchsten ID
        new_comment = Comment.objects.latest("id")
        self.assertEqual(new_comment.text, "Ein neuer Kommentar")
        self.assertEqual(new_comment.author, "Neuer Tester")


class AddArticleViewTests(TestCase):
    def test_add_article_view_get(self):
        response = self.client.get(reverse("add_article"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")

    def test_add_article_view_post(self):
        response = self.client.post(
            reverse("add_article"),
            {"title": "Neuer Artikel", "content": "Inhalt des neuen Artikels"},
        )
        self.assertEqual(response.status_code, 302)
        # Holt den zuletzt hinzugefügten Artikel aus der Datenbank basierend auf der höchsten ID
        new_article = Article.objects.latest("id")
        self.assertEqual(new_article.title, "Neuer Artikel")
        self.assertEqual(new_article.content, "Inhalt des neuen Artikels")

    def test_add_article_view_error(self):
        response = self.client.post(
            reverse("add_article"),
            {"title": "Neuer Artikel", "content": "Inhalt des neuen Artikels"},
        )
        self.assertEqual(response.status_code, 302)
        # Holt den zuletzt hinzugefügten Artikel aus der Datenbank basierend auf der höchsten ID
        new_article = Article.objects.latest("id")
        self.assertEqual(new_article.title, "Neuer Artikel")
        self.assertEqual(new_article.content, "Inhalt des neuen Artikels")