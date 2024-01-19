from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, UpdateView
from .models import UserProfile
from quiz.models import Subcategory
from django.urls import reverse_lazy
from .forms import ProfileUpdateForm

class UserProfileView(LoginRequiredMixin, TemplateView):
    model = UserProfile
    template_name = 'accounts/profile.html'

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_subcategories = Subcategory.objects.filter(creator=self.request.user)
        context['user_subcategories'] = user_subcategories
        return context  

class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    template_name = "accounts/profile_edit.html"
    form_class = ProfileUpdateForm
    
    def get_success_url(self):
        user_id = self.get_object().id
        return reverse_lazy('profile')

    def test_func(self):
        object_instance = self.get_object()
        return object_instance.user == self.request.user

    def form_valid(self, form):
        profile = form.save()
        user = profile.user
        user.username = form.cleaned_data["username"]
        return super().form_valid(form)