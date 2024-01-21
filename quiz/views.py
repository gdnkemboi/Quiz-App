from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from .models import Category, Subcategory, Question, Choice
from django.shortcuts import get_object_or_404, redirect, render
from .forms import SubcategoryForm, QuestionForm, ChoiceForm, ChoiceFormSet
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django import forms
from django.db.models import Count


class HomePageView(TemplateView):
    template_name = "quiz/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get 10 recently added subcategories
        recent_subcategories = Subcategory.objects.order_by("-created_at")[:10]

        # Get all categories together with four random sabcategories
        categories = Category.objects.all()
        categories_and_subcategories = []

        for category in categories:
            subcategories = Subcategory.objects.filter(category=category).order_by("?")[
                :4
            ]

            subcategory_count = Subcategory.objects.filter(category=category).count()

            categories_and_subcategories.append(
                {"category": category, "subcategories": subcategories, "subcategory_count": subcategory_count}
            )

        context["recent_subcategories"] = recent_subcategories
        context["categories_and_subcategories"] = categories_and_subcategories

        return context


class SubcategoryListView(ListView):
    model = Subcategory
    template_name = "quiz/category.html"
    context_object_name = "subcategories"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        category = get_object_or_404(Category, slug=slug)
        return Subcategory.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        category = get_object_or_404(Category, slug=slug)
        subcategories = Subcategory.objects.filter(category=category).annotate(question_count=Count('question'))
        context["category"] = category
        context["subcategories"] = subcategories
        return context


class SubcategoryDetailView(TemplateView):
    template_name = "quiz/subcategory.html"
    context_object_name = "subcategory"

    def get(self, request, *args, **kwargs):
        # Get the subcategory object using the provided pk
        subcategory = Subcategory.objects.get(pk=kwargs["pk"])

        # Get all questions and their choices related to this subcategory
        questions_and_choices = []
        questions = Question.objects.filter(sub_category=subcategory)

        for question in questions:
            choices = Choice.objects.filter(question=question)
            questions_and_choices.append({"question": question, "choices": choices})

        return render(
            request,
            self.template_name,
            {
                "subcategory": subcategory,
                "questions_and_choices": questions_and_choices,
            },
        )

    def post(self, request, *args, **kwargs):
        subcategory = Subcategory.objects.get(pk=kwargs["pk"])
        questions = Question.objects.filter(sub_category=subcategory)
        total_questions = questions.count()
        correct_answers = 0

        for question in questions:
            choice_id = request.POST.get(f"question_{question.id}")
            if choice_id:
                choice = Choice.objects.get(pk=choice_id)
                if choice.is_correct:
                    correct_answers += 1

        # Calculate the percentage of correct answers
        if total_questions > 0:
            percentage = (correct_answers / total_questions) * 100
        else:
            percentage = 0

        return render(request, "quiz/results.html", {"percentage": percentage})


class SubcategoryCreateView(LoginRequiredMixin, CreateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = "quiz/create_subcategory.html"

    def form_valid(self, form):
        subcategory = form.save(commit=False)
        subcategory.creator = self.request.user
        subcategory.save()
        subcategory_id = str(subcategory.id)
        self.success_url = reverse_lazy(
            "add_question", kwargs={"subcategory_id": subcategory_id}
        )
        return super().form_valid(form)


class AddQuestionView(LoginRequiredMixin, TemplateView):
    template_name = "quiz/add_question.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategory_id = self.kwargs.get("subcategory_id")
        subcategory = Subcategory.objects.get(id=subcategory_id)
        context["subcategory"] = subcategory
        context["question_form"] = QuestionForm
        context["choice_formset"] = ChoiceFormSet
        return context

    def post(self, request, *args, **kwargs):
        subcategory_id = self.kwargs.get("subcategory_id")
        subcategory = Subcategory.objects.get(id=subcategory_id)
        question_form = QuestionForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST)

        if question_form.is_valid() and choice_formset.is_valid():
            # Check if at least one choice is marked as correct
            has_correct_choice = False
            for form in choice_formset:
                if form.cleaned_data.get("is_correct"):
                    has_correct_choice = True
                    break

            if not has_correct_choice:
                # If no correct choice is selected, re-render the form with an error
                context = self.get_context_data()
                context["question_form"] = question_form
                context["choice_formset"] = choice_formset
                context[
                    "error_message"
                ] = "At least one choice must be marked as correct."
                return self.render_to_response(context)

            question = question_form.save(commit=False)
            question.sub_category = subcategory
            question.save()
            choice_formset.instance = question
            choice_formset.save()

            button_clicked = request.POST.get("save_add_another")
            if button_clicked:
                return redirect("add_question", subcategory_id=subcategory.id)
            else:
                return redirect("subcategory", pk=subcategory.id)

        else:
            context = self.get_context_data()
            context["question_form"] = question_form
            context["choice_formset"] = choice_formset

            # Check if ChoiceFormSet has errors due to insufficient choices
            if choice_formset.total_form_count() < 2:
                context["error_message"] = "At least two choices are required."

            return self.render_to_response(context)


class QuizUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = "quiz/update_quiz.html"

    def form_valid(self, form):
        subcategory = form.save(commit=False)
        subcategory.creator = self.request.user
        subcategory.save()
        subcategory_id = str(subcategory.id)
        self.success_url = reverse_lazy("subcategory", kwargs={"pk": subcategory_id})

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategory = self.get_object()
        questions_and_choices = []

        # Get all questions and their choices related to this subcategory
        questions = Question.objects.filter(sub_category=subcategory)

        for question in questions:
            choices = Choice.objects.filter(question=question)

            questions_and_choices.append({"question": question, "choices": choices})

        context["subcategory"] = subcategory
        context["questions_and_choices"] = questions_and_choices

        return context

    def test_func(self):
        obj = self.get_object()
        return obj.creator == self.request.user or self.request.user.is_superuser



class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "quiz/edit_question.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategory_id = self.kwargs.get("subcategory_id")
        context["subcategory_id"] = subcategory_id

        if self.request.POST:
            context["choice_formset"] = ChoiceFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["choice_formset"] = ChoiceFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        choice_formset = context["choice_formset"]

        if choice_formset.is_valid():
            # Check if at least one choice is marked as correct and at least two choices exist
            has_correct_choice = any(
                form.cleaned_data.get("is_correct") for form in choice_formset
            )
            choices_count = len(choice_formset.cleaned_data)

            if not has_correct_choice:
                context["error_message"] = "At least one choice must be marked as correct."
                return self.render_to_response(context)

            if choices_count < 2:
                context["error_message"] = "At least two choices are required."
                return self.render_to_response(context)

            choice_formset.save()

            self.success_url = reverse_lazy(
                "update_quiz", kwargs={"pk": context["subcategory_id"]}
            )
            return super().form_valid(form)
        else:
            context["error_message"] = "Error!"
            return self.render_to_response(context)


class SubcategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Subcategory
    success_url = reverse_lazy("home")
    template_name = "quiz/confirm_delete.html"

    def test_func(self):
        obj = self.get_object()
        return obj.creator == self.request.user or self.request.user.is_superuser


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = "quiz/confirm_delete.html"

    def get_success_url(self):
        subcategory_id = self.object.sub_category.id
        return reverse_lazy("subcategory", kwargs={"pk": subcategory_id})


class ChoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Choice
    template_name = "quiz/confirm_delete.html"

    def get_success_url(self):
        question = self.object.question
        question_id = question.id
        subcategory = question.sub_category
        return reverse_lazy(
            "edit_question",
            kwargs={"subcategory_id": subcategory.id, "pk": question_id},
        )
