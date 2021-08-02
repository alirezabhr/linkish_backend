# Generated by Django 3.2.5 on 2021-08-02 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('is_video', models.BooleanField()),
                ('image', models.FileField(upload_to='')),
                ('video', models.FileField(blank=True, upload_to='')),
                ('base_link', models.CharField(max_length=60)),
                ('clicks', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('max_budget', models.PositiveIntegerField()),
                ('is_general', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdViewerDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=80)),
                ('http_referer', models.CharField(max_length=60, null=True)),
                ('viewed_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='InfAd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clicks', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('short_link', models.CharField(blank=True, max_length=7)),
                ('approved_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SuggestAd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.BooleanField(default=False)),
                ('is_rejected', models.BooleanField(default=False)),
                ('is_reported', models.BooleanField(default=False)),
                ('report_msg', models.CharField(max_length=30, null=True)),
                ('suggested_at', models.DateTimeField(auto_now_add=True)),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ad.ad')),
            ],
        ),
    ]
