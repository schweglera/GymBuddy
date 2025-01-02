from django.test import TestCase
from ..models import Article, Comment
from django.core.exceptions import ValidationError


class ArticleModelTest(TestCase):
    def test_title_length_validators(self):
        article = Article(title="a" * 0, content="Valid Content" * 100)
        with self.assertRaises(ValidationError):
            article.full_clean()

        article = Article(title="a" * 101, content="Valid Content" * 100)
        with self.assertRaises(ValidationError):
            article.full_clean()

    def test_content_length_validators(self):
        article = Article(title="Valid Title", content="Short")
        with self.assertRaises(ValidationError):
            article.full_clean()

        article = Article(title="Valid Title", content="a" * 10001)
        with self.assertRaises(ValidationError):
            article.full_clean()


class CommentModelTest(TestCase):
    def setUp(self):
        self.article = Article(title="Valid Title", content="Valid Content" * 100)
        self.article.save()

    def test_author_name_length_validators(self):
        comment = Comment(article=self.article, author="a", text="Valid Comment" * 50)
        with self.assertRaises(ValidationError):
            comment.full_clean()

        comment = Comment(
            article=self.article, author="a" * 101, text="Valid Comment" * 50
        )
        with self.assertRaises(ValidationError):
            comment.full_clean()

    def test_comment_text_length_validators(self):
        comment = Comment(article=self.article, author="Valid Author", text="A")
        with self.assertRaises(ValidationError):
            comment.full_clean()

        comment = Comment(article=self.article, author="Valid Author", text="a" * 1001)
        with self.assertRaises(ValidationError):
            comment.full_clean()
