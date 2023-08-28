from django.contrib import admin
from .models import Category, Area, Faskes, Option, Survey, Question, Answer, Publication
from .mixins import BaseAdminMixin

# Inline admin classes
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

class PublicationInline(admin.StackedInline):
    model = Publication
    extra = 1

# Register your models with the admin site
@admin.register(Category)
class CategoryAdmin(BaseAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'created_by', 'updated_by', 'date_created', 'date_updated')

@admin.register(Area)
class AreaAdmin(BaseAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'code', 'type', 'parent', 'date_created', 'date_updated')

@admin.register(Faskes)
class FaskesesAdmin(BaseAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'location', 'date_created', 'date_updated')

@admin.register(Option)
class OptionAdmin(BaseAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'number', 'category','created_by', 'updated_by', 'date_created', 'date_updated')
    list_filter = ('category',)  # Add category to the list of filters

@admin.register(Survey)
class SurveyAdmin(BaseAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'survey_id', 'faskes', 'approved_by', 'created_by', 'date_created', 'date_updated')
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(BaseAdminMixin, admin.ModelAdmin):
    list_display = ('survey', 'question_text', 'date_created', 'date_updated')
    inlines = [AnswerInline]

@admin.register(Answer)
class AnswerAdmin(BaseAdminMixin, admin.ModelAdmin):
    list_display = ('respondent', 'question', 'choice', 'timestamp')

@admin.register(Publication)
class PublicationAdmin(BaseAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'category', 'created_by', 'date_created', 'date_updated')
    # Comment out the following line if you don't want the inline for Publication in SurveyAdmin
    # inlines = [PublicationInline]
