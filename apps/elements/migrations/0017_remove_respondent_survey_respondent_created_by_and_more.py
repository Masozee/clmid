# Generated by Django 4.2.4 on 2023-08-30 06:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('elements', '0016_respondent_survey'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='respondent',
            name='survey',
        ),
        migrations.AddField(
            model_name='respondent',
            name='created_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='respondent',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='respondent',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='respondent',
            name='keterangan',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='respondent',
            name='pengumpulan_data',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respondent',
            name='updated_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='respondent',
            name='nama',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.DeleteModel(
            name='Survey',
        ),
    ]
