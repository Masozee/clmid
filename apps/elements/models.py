from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from .mixins import UserStampedModel
from django.core.exceptions import ValidationError
import uuid
from django.db.models import F

class Category(UserStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategori"

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

    class Meta:
        verbose_name = "Provinsi/Kabupaten/Kota"
        verbose_name_plural = "Provinsi/Kabupaten/Kota"

class Faskes(UserStampedModel):
    name = models.CharField(max_length=200)
    location = models.ForeignKey(Area, verbose_name="Location Faskes", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Fasilitas Kesehatan"
        verbose_name_plural = "Fasilitas Kesehatan"
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

    class Meta:
        verbose_name = "Opsi jawaban"
        verbose_name_plural = "Opsi jawaban"

class Respondent(UserStampedModel):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    id_respondent = models.CharField(max_length=100, blank=True)
    usia = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="Usia_Category", limit_choices_to={'category__title': 'Usia'})
    gender = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="Gender_Category", limit_choices_to={'category__title': 'Gender'})
    faskes = models.ForeignKey(Faskes, on_delete=models.CASCADE)
    jarnas = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="Jarnas_Category", limit_choices_to={'category__title': 'Lembaga'})
    pengumpulan_data = models.DateTimeField(blank=True, null=True)
    keterangan = models.TextField(blank=True)


    def __str__(self):
        return self.id_respondent

    class Meta:
        verbose_name = "Responden Survey"
        verbose_name_plural = "Responden Survey"

class Question(UserStampedModel):
    kategori = models.ForeignKey(Option, on_delete=models.CASCADE, verbose_name="Survey Title", limit_choices_to={'category__title': 'Jenis Layanan'})
    code = models.CharField(max_length=10)
    question_text = models.TextField()
    answer_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategori Jawaban", related_name="Question_answer_Category",)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Pertanyaan Survey"
        verbose_name_plural = "Pertanyaan Survey"

class Answer(UserStampedModel):

    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE, related_name='survey_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(
        Option,
        on_delete=models.CASCADE,
        related_name="Answer_choices",
    )

    def __str__(self):
        return f"Answer by {self.respondent}"

    class Meta:
        verbose_name = "Jawaban Survey"
        verbose_name_plural = "Jawaban Survey"

class Publication(UserStampedModel):
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = HTMLField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_publications')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Publikasi"
        verbose_name_plural = "Publikasi"