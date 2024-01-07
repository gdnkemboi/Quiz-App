from django.urls import path
from .views import HomePageView, SubcategoryListView, SubcategoryDetailView, SubcategoryCreateView, AddQuestionView, QuizUpdateView, QuestionUpdateView, SubcategoryDeleteView, QuestionDeleteView, ChoiceDeleteView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("create-quiz/", SubcategoryCreateView.as_view(), name="create_quiz"),
    path("add-question/<uuid:subcategory_id>/", AddQuestionView.as_view(), name="add_question"),
    path("<slug:slug>/", SubcategoryListView.as_view(), name="category"),
    path("play/<uuid:pk>", SubcategoryDetailView.as_view(), name="subcategory"),
    path("edit/<uuid:pk>/", QuizUpdateView.as_view(), name="update_quiz"),
    path("edit/<uuid:subcategory_id>/<int:pk>/", QuestionUpdateView.as_view(), name="edit_question"),
    path("<uuid:pk>/delete/", SubcategoryDeleteView.as_view(), name="subcategory_delete"),
    path("<int:pk>/delete/", QuestionDeleteView.as_view(), name="question_delete"),
    path("choice/<int:pk>/delete/", ChoiceDeleteView.as_view(), name="choice_delete"),
]
