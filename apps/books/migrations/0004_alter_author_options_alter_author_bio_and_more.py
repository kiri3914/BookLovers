# Generated by Django 4.2.5 on 2023-09-26 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_author_birth_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': 'Автор', 'verbose_name_plural': 'Авторы'},
        ),
        migrations.AlterField(
            model_name='author',
            name='bio',
            field=models.TextField(blank=True, verbose_name='Биография'),
        ),
        migrations.AlterField(
            model_name='author',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='author',
            name='death_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата смерти'),
        ),
        migrations.AlterField(
            model_name='author',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='author',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='Фамилия'),
        ),
    ]
