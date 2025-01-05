from django.test import TestCase
from ..forms import ArticleForm, CommentForm


class ArticleFormTest(TestCase):
    def test_article_form_valid_data(self):
        form = ArticleForm(data={"title": "Valider Titel", "content": "Valider Inhalt"})
        self.assertTrue(form.is_valid())

    def test_article_form_forbidden_word_in_title(self):
        form = ArticleForm(
            data={"title": "unangemessenesWort1 ist hier", "content": "Valider Inhalt"}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["title"], ["Unangemessenes Wort im Titel gefunden."]
        )

    def test_article_form_forbidden_word_in_content(self):
        form = ArticleForm(
            data={"title": "Valider Titel", "content": "Hier ist unangemessenesWort2"}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["content"], ["Unangemessenes Wort im Inhalt gefunden."]
        )


class CommentFormTest(TestCase):
    def test_comment_form_valid_data(self):
        form = CommentForm(data={"author": "Valider Autor", "text": "Valider Text"})
        self.assertTrue(form.is_valid())

    def test_comment_form_forbidden_word_in_author(self):
        form = CommentForm(
            data={"author": "unangemessenesWort3", "text": "Valider Text"}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["author"], ["Autorname enthält unangemessenes Wort."]
        )

    def test_comment_form_forbidden_word_in_text(self):
        form = CommentForm(
            data={"author": "Valider Autor", "text": "Das ist unangemessenesWort1"}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], ["Unangemessenes Wort im Text gefunden."])
