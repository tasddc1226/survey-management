# Generated by Django 4.0.5 on 2022-06-09 14:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_alter_question_answer_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='phone',
            field=models.CharField(default=1234, max_length=16, unique=True, validators=[django.core.validators.RegexValidator(regex='^?1?\\d{8,15}$')]),
            preserve_default=False,
        ),
    ]
