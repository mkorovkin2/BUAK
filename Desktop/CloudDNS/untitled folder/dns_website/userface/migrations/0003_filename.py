# Generated by Django 3.0.7 on 2020-06-25 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userface', '0002_delete_upload'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filename',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('filename', models.CharField(max_length=200)),
            ],
        ),
    ]