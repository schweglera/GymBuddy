from django.test import TestCase
from django.urls import reverse
from django.utils.html import escape
from ..models import Article, Comment, MealPlan, TrainingPlan, Workout, Exercise
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta



class ArticleListViewTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title="Test Article", content="Test content for article."
        )
        self.user = User.objects.create_user(
            username='testuser', password='password123'
        )
        self.client.force_login(self.user)

    def test_article_list_view_renders_correctly(self):
        response = self.client.get(reverse("article_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Willkommen bei Gym-Buddy!")
        self.assertContains(response, self.article.title)

    def test_article_list_view_no_articles(self):
        Article.objects.all().delete()
        response = self.client.get(reverse("article_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Willkommen bei Gym-Buddy!")
        self.assertContains(response, "Keine Artikel verfügbar.")
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


#Testing the Authentication Views
class AuthenticationViewsTests(TestCase):
    def test_login_view_renders_correctly(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_register_view_get(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_register_view_post(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "password1": "testpassword123",
            "password2": "testpassword123"
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.assertTrue(User.objects.filter(username="newuser").exists())


#Testing Dashboard
class DashboardViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.force_login(self.user)

    def test_dashboard_view_renders_correctly(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/dashboard.html")


#Tests for Workouts
class WorkoutViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_login(self.user)
        self.workout = Workout.objects.create(
            user=self.user, workout_type="Cardio", duration=timedelta(minutes=30)
        )
        Exercise.objects.create(
            workout=self.workout, name="Pushups", sets=3, reps=15, weight=0
        )

    def test_workout_list_view(self):
        response = self.client.get(reverse("all_workouts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/all_workouts.html")
        self.assertContains(response, "Cardio")

    def test_workout_detail_view(self):
        response = self.client.get(reverse("workout_detail", args=[self.workout.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "workout_detail.html")
        self.assertContains(response, "Cardio")
        self.assertContains(response, "Pushups")

    def test_workout_create_view_get(self):
        response = self.client.get(reverse("workout_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "workout_create.html")

    def test_workout_create_view_post(self):
        response = self.client.post(reverse("workout_create"), {
            "workout_type": "Strength",
            "duration": "00:45:00",
            "date": date.today(),
            "form-INITIAL_FORMS": 0,
            "form-TOTAL_FORMS": 1,
            "form-0-name": "Squats",
            "form-0-sets": 3,
            "form-0-reps": 12,
            "form-0-weight": 100,
        })

        # Check if formset or form has validation issues
        if response.status_code == 200:  # If not redirected, check for errors
            print("Workout form errors:", response.context['workout_form'].errors)
            print("Exercise formset errors:", response.context['exercise_formset'].errors)

        self.assertEqual(response.status_code, 302)  # Expect redirect
        self.assertTrue(Workout.objects.filter(workout_type="Strength").exists())
        self.assertTrue(Exercise.objects.filter(name="Squats").exists())

class WorkoutListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.force_login(self.user)
        self.workout = Workout.objects.create(
            user=self.user,
            workout_type="Cardio",
            duration=timedelta(minutes=30),
            date=date.today()
        )

    def test_workout_list_view(self):
        response = self.client.get(reverse("all_workouts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/all_workouts.html")
        self.assertContains(response, self.workout.workout_type)


#Tests for Training Plans
class TrainingPlanViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.force_login(self.user)
        self.training_plan = TrainingPlan.objects.create(
            user=self.user,
            name="Strength Plan",
            category="Strength",
            exercise1="Bench Press",
            exercise2="Deadlift",
        )

    def test_training_plan_list_view(self):
        response = self.client.get(reverse("all_tplan"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/all_tplan.html")
        self.assertContains(response, "Strength Plan")

    def test_training_plan_detail_view(self):
        response = self.client.get(reverse("tplan_detail", args=[self.training_plan.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/tplan_detail.html")
        self.assertContains(response, "Strength Plan")
        self.assertContains(response, "Bench Press")

    def test_training_plan_create_view_get(self):
        response = self.client.get(reverse("tplan_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tplan_create.html")

    def test_training_plan_create_view_post(self):
        response = self.client.post(reverse("tplan_create"), {
            "name": "Endurance Plan",
            "category": "Endurance",
            "exercise1": "Running",
            "exercise2": "Cycling",
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to dashboard
        self.assertTrue(TrainingPlan.objects.filter(name="Endurance Plan").exists())


#Tests for Meal Plans
class MealPlanViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.force_login(self.user)
        self.meal_plan = MealPlan.objects.create(
            user=self.user,
            name="Weight Loss Plan",
            breakfast="Oatmeal",
            lunch="Grilled Chicken Salad",
            dinner="Steamed Vegetables",
            calories=1500,
        )

    def test_meal_plan_list_view(self):
        response = self.client.get(reverse("all_mplan"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/all_mplan.html")
        self.assertContains(response, "Weight Loss Plan")

    def test_meal_plan_detail_view(self):
        response = self.client.get(reverse("mplan_detail", args=[self.meal_plan.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/mplan_detail.html")
        self.assertContains(response, "Weight Loss Plan")
        self.assertContains(response, "Oatmeal")

    def test_meal_plan_create_view_get(self):
        response = self.client.get(reverse("mplan_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mplan_create.html")

    def test_meal_plan_create_view_post(self):
        response = self.client.post(reverse("mplan_create"), {
            "name": "Muscle Gain Plan",
            "breakfast": "Eggs and Toast",
            "lunch": "Chicken Breast",
            "dinner": "Salmon and Quinoa",
            "calories": 2500,
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to dashboard
        self.assertTrue(MealPlan.objects.filter(name="Muscle Gain Plan").exists())

    class MealPlanDetailViewTests(TestCase):
        def setUp(self):
            self.user = User.objects.create_user(username="testuser", password="password123")
            self.meal_plan = MealPlan.objects.create(user=self.user, name="My Meal Plan", calories=2000)
            self.client.force_login(self.user)

        def test_mplan_detail_view(self):
            response = self.client.get(reverse("mplan_detail", args=[self.meal_plan.pk]))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "user/mplan_detail.html")
            self.assertContains(response, "My Meal Plan")


    #Tests for Coaches
    class CoachViewsTests(TestCase):
        def setUp(self):
            self.coach = Coach.objects.create(
                name="John Doe",
                category="Fitness",
                bio="Certified personal trainer",
                experience=5,
                price_hour=50,
                email="john.doe@example.com",
            )

        def test_coach_list_view(self):
            response = self.client.get(reverse("all_coach"))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "all_coach.html")
            self.assertContains(response, "John Doe")

        def test_coach_detail_view(self):
            response = self.client.get(reverse("coach_detail", args=[self.coach.pk]))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "coach_detail.html")
            self.assertContains(response, "John Doe")
            self.assertContains(response, "Certified personal trainer")

    class CoachCreateViewTests(TestCase):
        def setUp(self):
            self.user = User.objects.create_user(username="adminuser", password="password123")
            self.admin_group = Group.objects.create(name="Admin")
            self.admin_group.user_set.add(self.user)
            self.client.force_login(self.user)

        def test_coach_create_view_get(self):
            response = self.client.get(reverse("coach_create"))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "coach_create.html")

        def test_coach_create_view_post(self):
            response = self.client.post(reverse("coach_create"), {
                "name": "Jane Doe",
                "category": "Yoga",
                "bio": "Certified yoga instructor",
                "experience": 10,
                "price_hour": 60,
                "email": "jane.doe@example.com",
            })
            self.assertEqual(response.status_code, 302)
            self.assertTrue(Coach.objects.filter(name="Jane Doe").exists())


#Tests for Community
    class CommunityViewTests(TestCase):
        def setUp(self):
            self.article = Article.objects.create(title="Community Post", content="Shared in the community.")
            self.user = User.objects.create_user(username="testuser", password="password123")
            self.client.force_login(self.user)

        def test_community_view(self):
            response = self.client.get(reverse("all_community"))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "all_community.html")
            self.assertContains(response, "Community Post")

        def test_community_view_renders_correctly(self):
            response = self.client.get(reverse("all_community"))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "all_community.html")
            self.assertContains(response, "Community Post")


# Tests for Admin
    class IsAdminTests(TestCase):
        def setUp(self):
            self.user = User.objects.create_user(username="testuser", password="password123")
            self.admin_group = Group.objects.create(name="Admin")
            self.admin_group.user_set.add(self.user)

        def test_is_admin(self):
            self.client.force_login(self.user)
            self.assertTrue(self.user.groups.filter(name="Admin").exists())

    class AdminRegisterViewTests(TestCase):
        def test_adminregister_get(self):
            response = self.client.get(reverse("adminregister"))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "adminregister.html")

        def test_adminregister_post(self):
            response = self.client.post(reverse("adminregister"), {
                "username": "adminuser",
                "password1": "ComplexPass123",
                "password2": "ComplexPass123",
            })
            self.assertEqual(response.status_code, 302)
            self.assertTrue(User.objects.filter(username="adminuser").exists())











