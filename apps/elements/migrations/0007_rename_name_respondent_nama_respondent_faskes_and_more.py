# Generated by Django 4.2.4 on 2023-08-29 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elements', '0006_respondent_remove_answer_user_answer_respondent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='respondent',
            old_name='name',
            new_name='nama',
        ),
        migrations.AddField(
            model_name='respondent',
            name='faskes',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='elements.faskes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='respondent',
            name='gender',
            field=models.ForeignKey(default=1, limit_choices_to={'category': 'Gender'}, on_delete=django.db.models.deletion.CASCADE, related_name='Gender_Category', to='elements.option'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='respondent',
            name='jarnas',
            field=models.ForeignKey(default=1, limit_choices_to={'category': 'Lembaga'}, on_delete=django.db.models.deletion.CASCADE, related_name='Jarnas_Category', to='elements.option'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='respondent',
            name='usia',
            field=models.ForeignKey(default=1, limit_choices_to={'category': 'Usia'}, on_delete=django.db.models.deletion.CASCADE, related_name='Usia_Category', to='elements.option'),
            preserve_default=False,
        ),
    ]