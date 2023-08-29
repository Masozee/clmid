from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from .mixins import UserStampedModel
from django.core.exceptions import ValidationError

class Category(UserStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Area(UserStampedModel):
    AREA_CATEGORY = (
        ('0', 'Provinsi'),
        ('1', 'Kabupaten'),
        ('2', 'Kota'),
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=1, choices=AREA_CATEGORY)
    parent = models.ForeignKey("self", limit_choices_to={'type': '0'}, verbose_name="Parent Area", on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Faskes(UserStampedModel):
    name = models.CharField(max_length=200)
    location = models.ForeignKey(Area, verbose_name="Location Faskes", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Option(UserStampedModel):
    name = models.CharField(max_length=250)
    number = models.IntegerField(editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Value Category")
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            last_option = Option.objects.filter(category=self.category).order_by('-number').first()
            if last_option:
                self.number = last_option.number + 1
            else:
                self.number = 1

        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

class Survey(UserStampedModel):
    STATUS_CHOICES = (
        ('approved', 'Approved'),
        ('reviewed', 'Reviewed'),
        ('rejected', 'Rejected'),
    )

    title = models.CharField(max_length=250)
    survey_id = models.CharField(max_length=10, unique=True)
    faskes = models.ForeignKey(Faskes, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_surveys')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_surveys')

    def generate_unique_survey_id(self):
        length = 9
        while True:
            random_id = ''.join(random.choices(string.digits, k=length))
            if not Survey.objects.filter(survey_id=random_id).exists():
                return random_id

    def set_status(self, new_status, user):
        self.status = new_status
        self.approved_by = user
        self.save()

    def __str__(self):
        return self.title

class Respondent(models.Model):


    nama = models.CharField(max_length=100)
    usia = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="Usia_Category", limit_choices_to={'category__title': 'Usia'})
    gender = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="Gender_Category", limit_choices_to={'category__title': 'Gender'})
    faskes = models.ForeignKey(Faskes, on_delete=models.CASCADE)
    jarnas = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="Jarnas_Category", limit_choices_to={'category__title': 'Lembaga'})


    def __str__(self):
        return self.nama

class Question(UserStampedModel):
    survey = models.ForeignKey(Option, on_delete=models.CASCADE, verbose_name="Survey Title", limit_choices_to={'category__title': 'Jenis Layanan'})
    code = models.CharField(max_length=10)
    question_text = models.TextField()
    answer_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategori Jawaban", related_name="Question_answer_Category",)

    def __str__(self):
        return self.code

class Answer(UserStampedModel):

    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE, related_name='survey_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="Answer_choices")

    def get_limit_choices_to(self):
        return {'category__title': self.question.answer_category.title}

    def __str__(self):
        return f"Answer by {self.respondent} to '{self.question.survey.name}'"

class Publication(UserStampedModel):
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = HTMLField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_publications')

    def __str__(self):
        return self.title
