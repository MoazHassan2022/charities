# Generated by Django 3.2.5 on 2021-09-09 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0009_alter_charity_slogan'),
    ]

    operations = [
        migrations.CreateModel(
            name='OneTimeLinkModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oneTimeCode', models.CharField(max_length=10)),
            ],
        ),
    ]
