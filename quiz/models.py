from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)   
    name = models.CharField(max_length=100)
    cover = models.ImageField(upload_to="covers/", blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"

class Question(models.Model):
    sub_category = models.ForeignKey(Subcategory, on_delete=models.CASCADE, default="")
    text = models.TextField(blank=True)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
