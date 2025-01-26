from django.test import TestCase
from ..models import Article, Comment, Workout, Exercise, MealPlan, TrainingPlan, Coach
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import date, timedelta



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


class WorkoutModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_workout_creation(self):
        workout = Workout(user=self.user, workout_type="Ausdauer", duration="01:00:00")
        workout.full_clean()  
        self.assertEqual(workout.workout_type, "Ausdauer")

class ExerciseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.workout = Workout.objects.create(
            user=self.user,
            workout_type="Kraft",
            duration=timedelta(minutes=30)
        )

    def test_exercise_creation(self):
        exercise = Exercise.objects.create(
            workout=self.workout,
            name="Squats",
            sets=3,
            reps=12,
            weight=100.0
        )
        exercise.full_clean()  
        self.assertEqual(exercise.name, "Squats")


class MealPlanModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_meal_plan_creation(self):
        meal_plan = MealPlan.objects.create(
            user=self.user,
            name="Gewichtsverlustplan",
            lunch="Salat mir Poulet",
            dinner="Suppe",
            calories=1200,
        )
        meal_plan.full_clean()  
        self.assertEqual(meal_plan.name, "Gewichtsverlustplan")


class TrainingPlanModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_training_plan_creation(self):
        training_plan = TrainingPlan.objects.create(
            user=self.user,
            name="Kraft Plan",
            category="Kraft",
            exercise1="Squats",
            exercise2="Deadlifts"
        )
        training_plan.full_clean()  
        self.assertEqual(training_plan.name, "Kraft Plan")


class CoachModelTest(TestCase):
    def test_coach_creation(self):
        coach = Coach.objects.create(
            name="Max Muster",
            category="Fitness",
            bio="Zertifizierter Personal Trainer",
            experience=5,
            price_hour=50,
            email="max.muster@example.com",
        )
        coach.full_clean()  
        self.assertEqual(coach.name, "Max Muster")