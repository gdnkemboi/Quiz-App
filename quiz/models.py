import uuid
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Subcategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True, blank=False)
    cover = models.ImageField(upload_to="covers/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"

    def get_absolute_url(self):
        return reverse("subcategory", args=[str(self.id)])

class Question(models.Model):
    sub_category = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    text = models.TextField(blank=False)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, blank=False)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
