# Generated by Django 4.1.2 on 2022-10-18 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0027_alter_balance_id_alter_savings_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='savings',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
