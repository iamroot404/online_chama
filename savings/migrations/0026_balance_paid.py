# Generated by Django 4.1.2 on 2022-10-14 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0025_remove_balance_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='paid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='savings.savings'),
        ),
    ]