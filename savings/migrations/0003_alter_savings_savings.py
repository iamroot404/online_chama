# Generated by Django 4.1.2 on 2022-10-13 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0002_savings_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savings',
            name='savings',
            field=models.CharField(default=0, max_length=100),
        ),
    ]
