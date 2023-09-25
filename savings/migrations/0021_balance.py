# Generated by Django 4.1.2 on 2022-10-13 17:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0020_delete_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('balance', models.IntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('paid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='savings.savings')),
            ],
        ),
    ]