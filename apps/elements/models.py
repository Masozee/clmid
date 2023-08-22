from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import random
import string
from django.contrib.auth.models import User

# Create your models here.
class Categories(models.Model):
    judul = models.CharField(max_length=200)
    keterangan = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.judul
    
class Area(models.Model):
    AREA_CATEGORY = (
        ('0', 'Provinsi'),
        ('1', 'Kabupaten'),
        ('2', 'Kota'),
    )
    nama = models.CharField(max_length=200)
    kode = models.CharField(max_length=10, blank=True, null=True)
    tipe = models.CharField(max_length=1, choices=AREA_CATEGORY)
    parent = models.ForeignKey("self", limit_choices_to={'tipe': '0'}, verbose_name="Parent Area", on_delete=models.CASCADE, blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama

class Faskes(models.Model):
    nama = models.CharField(max_length=200)
    lokasi = models.ForeignKey(Area, verbose_name="Lokasi Faskes", on_delete=models.CASCADE)
    keterangan = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama
    

class Option(models.Model):
    nama = models.CharField(max_length=250)
    nomor = models.IntegerField()
    kategori = models.ForeignKey("Categories", on_delete=models.CASCADE, verbose_name="Kategori Nilai")
    keterangan = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama

class Survey(models.Model):
    STATUS_CHOICES = (
        ('approved', 'Approved'),
        ('reviewed', 'Reviewed'),
        ('rejected', 'Rejected'),
    )

    judul = models.CharField(max_length=250)
    survey_id = models.CharField(max_length=10, unique=True)
    faskes = models.ForeignKey(Faskes, on_delete=models.CASCADE, null=True, blank=True)
    keterangan = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_surveys')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_surveys')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        request = kwargs.pop('request', None)

        if request:
            if not self.id:  # New instance, set created_by and created timestamp
                self.created_by = request.user
            else:  # Existing instance, set approved_by and modified timestamp
                self.approved_by = request.user
                self.date_modified = timezone.now()

        if not self.survey_id:
            self.survey_id = self.generate_unique_survey_id()

        super(Survey, self).save(*args, **kwargs)

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
        return self.judul

class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name="judul survey")
    question_text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    CHOICES = (
        (1, 'Ya'),
        (0, 'Tidak'),
        (99, 'Tidak Menjawab'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='survey_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.IntegerField(choices=CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user.username} to '{self.survey.title}'"

    