# Generated by Django 3.2.5 on 2021-08-03 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20210801_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default-profile.jpg', upload_to=''),
        ),
    ]
