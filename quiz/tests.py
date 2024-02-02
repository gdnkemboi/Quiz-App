from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category, Subcategory, Question, Choice
from .views import HomePageView

class QuizViewsTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.subcategory = Subcategory.objects.create(
            category=self.category,
            name='Test Subcategory',
            creator=self.user
        )
        self.question = Question.objects.create(sub_category=self.subcategory, text='Test Question')
        self.choice = Choice.objects.create(question=self.question, text='Test Choice', is_correct=True)

    def test_home_page_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_view_get_context_data(self):
        view = HomePageView()
        context = view.get_context_data()

        # Check if the context contains the expected keys
        self.assertIn('recent_subcategories', context)
        self.assertIn('categories_and_subcategories', context)

        # Check if the context values are correct
        self.assertEqual(len(context['recent_subcategories']), 1)
        self.assertEqual(len(context['categories_and_subcategories']), 1)

    def test_subcategory_list_view(self):
        url = reverse('category', args=['test-category'])
        response = self.client.get(url)
        view = response.context['view']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(view.kwargs['slug'], 'test-category')

        # Check if 'category' and 'subcategories' are present in the context
        self.assertIn('category', response.context)
        self.assertIn('subcategories', response.context)

        # Check if 'category' is the correct Category object
        self.assertEqual(response.context['category'], self.category)

        # Check if 'subcategories' contains the correct Subcategory objects
        subcategories = response.context['subcategories']
        self.assertIn(self.subcategory, subcategories)

    def test_subcategory_detail_view(self):
        response = self.client.get(reverse('subcategory', args=[str(self.subcategory.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Subcategory')  # Check if the subcategory name is present in the response content
        self.assertContains(response, 'Test Question')  # Check if the question text is present in the response content

    def test_subcategory_detail_view_post(self):
        response = self.client.post(reverse('subcategory', args=[str(self.subcategory.id)]), {
            f"question_{self.question.id}": str(self.choice.id),
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Results')  # Check if the "Results" string is present in the response content

    def test_subcategory_create_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('create_quiz'))
        self.assertEqual(response.status_code, 200)

    def test_subcategory_delete_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('subcategory_delete', args=[str(self.subcategory.id)]))
        self.assertEqual(response.status_code, 200)

    def test_question_delete_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('question_delete', args=[str(self.question.id)]))
        self.assertEqual(response.status_code, 200)

    def test_choice_delete_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('choice_delete', args=[str(self.choice.id)]))
        self.assertEqual(response.status_code, 200)