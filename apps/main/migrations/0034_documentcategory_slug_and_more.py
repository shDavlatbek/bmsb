# Generated by Django 5.2.1 on 2025-07-02 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_documentcategory_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentcategory',
            name='slug',
            field=models.SlugField(default='', verbose_name='Slug'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='documentcategory',
            constraint=models.UniqueConstraint(fields=('school', 'slug'), name='unique_document_category_school_slug'),
        ),
    ]
