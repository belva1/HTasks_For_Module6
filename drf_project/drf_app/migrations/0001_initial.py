# Generated by Django 4.2.5 on 2023-09-04 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, verbose_name='Gender')),
                ('age', models.PositiveIntegerField(verbose_name='Age')),
                ('english_level', models.CharField(choices=[('A1', 'Beginner'), ('A2', 'Pre-Intermediate'), ('B1', 'Intermediate'), ('B2', 'Upper-Intermediate'), ('C1', 'Advanced'), ('C2', 'Proficiency')], max_length=12, verbose_name='English Level')),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'People',
            },
        ),
    ]