# Generated by Django 5.2.1 on 2025-06-01 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_faq'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'verbose_name': "Ko'p so'raladigan savol ", 'verbose_name_plural': "Ko'p so'raladigan savollar"},
        ),
        migrations.AlterUniqueTogether(
            name='faq',
            unique_together=set(),
        ),
    ]
