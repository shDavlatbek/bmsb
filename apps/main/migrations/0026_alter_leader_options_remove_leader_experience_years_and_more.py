# Generated by Django 5.2.1 on 2025-06-04 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_leader_staff'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leader',
            options={'verbose_name': 'Rahbar ', 'verbose_name_plural': 'Rahbarlar'},
        ),
        migrations.RemoveField(
            model_name='leader',
            name='experience_years',
        ),
        migrations.RemoveField(
            model_name='leader',
            name='order',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='description',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='description_ru',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='description_uz',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='email',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='leader',
            name='working_days',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ish kunlari'),
        ),
        migrations.AddField(
            model_name='leader',
            name='working_days_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ish kunlari'),
        ),
        migrations.AddField(
            model_name='leader',
            name='working_days_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ish kunlari'),
        ),
        migrations.AddField(
            model_name='leader',
            name='working_days_uz',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ish kunlari'),
        ),
    ]
