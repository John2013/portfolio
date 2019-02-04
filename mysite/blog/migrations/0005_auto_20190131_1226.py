# Generated by Django 2.1.5 on 2019-01-31 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_article_preview'),
    ]

    # noinspection PyUnresolvedReferences
    operations = [
        migrations.AlterField(
            model_name='article',
            name='body',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.CharField(default='', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(
                related_query_name='Теги', to='blog.Tag'
            ),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.CharField(default='', max_length=255, unique=True),
        ),
    ]
