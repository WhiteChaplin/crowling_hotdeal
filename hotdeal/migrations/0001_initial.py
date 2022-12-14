# Generated by Django 4.1.3 on 2022-12-09 10:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=200)),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.CharField(default='', max_length=10, null=True)),
                ('price', models.IntegerField(null=True)),
                ('site', models.CharField(default=0, max_length=20)),
            ],
        ),
    ]
