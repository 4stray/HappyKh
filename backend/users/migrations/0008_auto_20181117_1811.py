# Generated by Django 2.1.2 on 2018-11-17 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20181029_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('W', 'woman'), ('M', 'man'), ('O', 'other'), ('U', 'unknown')], default='U', max_length=2),
        ),
    ]
