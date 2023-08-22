from django.contrib import admin
from .models import Categories, Area, Faskes, Option, Survey, Question, Answer

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    readonly_fields = ('get_survey_title', 'get_survey_faskes', 'get_question_text')

    def get_survey_title(self, obj):
        return obj.question.survey.judul
    get_survey_title.short_description = 'Survey Title'

    def get_survey_faskes(self, obj):
        return obj.question.survey.faskes.nama if obj.question.survey.faskes else '-'
    get_survey_faskes.short_description = 'Survey Faskes'

    def get_question_text(self, obj):
        return obj.question.question_text
    get_question_text.short_description = 'Question Text'

class FaskesInline(admin.TabularInline):
    model = Faskes
    extra = 1
    inlines = [QuestionInline]

class SurveyInline(admin.TabularInline):
    model = Survey
    extra = 1
    inlines = [QuestionInline]

class AreaInline(admin.TabularInline):
    model = Area
    extra = 1
    inlines = [FaskesInline]

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('judul', 'date_created', 'date_modified')
    inlines = [OptionInline]

class AreaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'tipe', 'parent', 'date_created', 'date_modified')
    inlines = [FaskesInline]

class FaskesAdmin(admin.ModelAdmin):
    list_display = ('nama', 'lokasi', 'date_created', 'date_modified')
    inlines = [SurveyInline]

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('judul', 'survey_id', 'approved_by', 'created_by', 'date_created', 'date_modified')
    list_filter = ('approved_by', 'created_by', 'date_created', 'date_modified')
    search_fields = ('judul', 'survey_id', 'approved_by__username', 'created_by__username')
    inlines = [QuestionInline]

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'survey', 'date_created', 'date_modified')
    inlines = [AnswerInline]

# Register the models and their respective admins
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Faskes, FaskesAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
