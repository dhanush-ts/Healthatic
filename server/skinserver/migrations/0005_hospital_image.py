# Generated by Django 5.0.7 on 2024-10-09 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skinserver', '0004_remove_hospital_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='image',
            field=models.ImageField(default=None, upload_to=''),
            preserve_default=False,
        ),
    ]
