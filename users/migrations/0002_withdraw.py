# Generated by Django 3.2.5 on 2021-07-28 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('is_paid', models.BooleanField(default=False)),
                ('request_at', models.DateTimeField(auto_now_add=True)),
                ('influencer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.influencer')),
            ],
        ),
    ]