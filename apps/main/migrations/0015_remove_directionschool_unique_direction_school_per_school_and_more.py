# Generated by Django 5.2.1 on 2025-05-28 05:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_teacher_directions_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='directionschool',
            name='unique_direction_school_per_school',
        ),
        migrations.AlterField(
            model_name='directionschool',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='directions', to='main.school', verbose_name='Maktab'),
        ),
    ]
