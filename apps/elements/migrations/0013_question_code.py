# Generated by Django 4.2.4 on 2023-08-29 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elements', '0012_alter_question_answer_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='code',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
