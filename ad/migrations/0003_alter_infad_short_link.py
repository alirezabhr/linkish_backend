# Generated by Django 3.2.5 on 2021-07-08 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infad',
            name='short_link',
            field=models.CharField(max_length=7),
        ),
    ]
