# Generated by Django 5.2.1 on 2025-06-04 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_alter_leader_options_remove_leader_experience_years_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='banner',
            unique_together={('school', 'title')},
        ),
        migrations.AlterUniqueTogether(
            name='document',
            unique_together={('school', 'title')},
        ),
        migrations.AlterUniqueTogether(
            name='faq',
            unique_together={('school', 'title')},
        ),
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together={('school', 'title', 'parent')},
        ),
        migrations.AlterUniqueTogether(
            name='schoollife',
            unique_together={('school', 'title')},
        ),
        migrations.AlterUniqueTogether(
            name='teacher',
            unique_together={('school', 'slug')},
        ),
    ]
