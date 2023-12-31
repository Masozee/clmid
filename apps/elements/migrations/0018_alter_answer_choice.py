# Generated by Django 4.2.4 on 2023-08-30 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elements', '0017_remove_respondent_survey_respondent_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='choice',
            field=models.ForeignKey(limit_choices_to=models.Q(('category', models.F('question__answer_category'))), on_delete=django.db.models.deletion.CASCADE, related_name='Answer_choices', to='elements.option'),
        ),
    ]
