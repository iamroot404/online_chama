# Generated by Django 4.1.2 on 2022-10-13 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0004_alter_savings_savings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savings',
            name='transaction_id',
            field=models.CharField(max_length=200),
        ),
    ]
