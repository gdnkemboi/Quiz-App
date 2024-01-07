from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import UserProfile
from quiz.models import Subcategory

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