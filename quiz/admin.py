from django.contrib import admin

from .models import Category, Question, Choice, Subcategory


class ChoiceInline(admin.TabularInline):  # or admin.StackedInline
    model = Choice
    extra = 3  # Number of extra Choice fields to display


class QuestionInline(admin.TabularInline):  # or admin.StackedInline
    model = Question
    extra = 0  # Number of extra Question fields to display

class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubcategoryInline]

class SubcategoryAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ("text", "sub_category")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
