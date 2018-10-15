# Generated by Django 2.1.1 on 2018-09-03 13:10

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('password',
                 models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True,
                                                    verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                (
                'age', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('gender',
                 models.CharField(choices=[('Ж', 'woman'), ('М', 'man')],
                                  default='Ж', max_length=2)),
                ('profile_image',
                 models.ImageField(blank=True, null=True, upload_to='')),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
