# Generated by Django 5.0.7 on 2024-10-09 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skinserver', '0005_hospital_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='image',
            field=models.URLField(),
        ),
    ]
