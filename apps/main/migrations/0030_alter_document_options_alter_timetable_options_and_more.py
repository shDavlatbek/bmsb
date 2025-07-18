# Generated by Django 5.2.1 on 2025-06-13 20:23

import apps.common.utils
import apps.common.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_merge_20250614_0031'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'verbose_name': 'Hujjat ', 'verbose_name_plural': 'Hujjatlar'},
        ),
        migrations.AlterModelOptions(
            name='timetable',
            options={'ordering': ['title'], 'verbose_name': "O'quv reja ", 'verbose_name_plural': "O'quv reja"},
        ),
        # Skip constraint removal - those constraints don't exist in the database
        # Original field operations
        migrations.RemoveField(
            model_name='direction',
            name='image',
        ),
        migrations.RemoveField(
            model_name='musicalinstrument',
            name='image',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='image',
        ),
        migrations.AddField(
            model_name='direction',
            name='background_image',
            field=models.ImageField(blank=True, help_text="Rasm 5 MB dan katta bo'lishi mumkin emas.", null=True, upload_to=apps.common.utils.generate_upload_path, validators=[apps.common.validators.file_size], verbose_name='Fon rasmi'),
        ),
        migrations.AddField(
            model_name='musicalinstrument',
            name='background_image',
            field=models.ImageField(blank=True, help_text="Rasm 5 MB dan katta bo'lishi mumkin emas.", null=True, upload_to=apps.common.utils.generate_upload_path, validators=[apps.common.validators.file_size], verbose_name='Fon rasmi'),
        ),
        migrations.AddField(
            model_name='musicalinstrument',
            name='icon',
            field=models.ImageField(blank=True, help_text="Rasm 5 MB dan katta bo'lishi mumkin emas.", null=True, upload_to=apps.common.utils.generate_upload_path, validators=[apps.common.validators.file_size], verbose_name='Ikonka'),
        ),
        migrations.AddField(
            model_name='subject',
            name='background_image',
            field=models.ImageField(blank=True, help_text="Rasm 5 MB dan katta bo'lishi mumkin emas.", null=True, upload_to=apps.common.utils.generate_upload_path, validators=[apps.common.validators.file_size], verbose_name='Fon rasmi'),
        ),
        migrations.AddField(
            model_name='subject',
            name='icon',
            field=models.ImageField(blank=True, help_text="Rasm 5 MB dan katta bo'lishi mumkin emas.", null=True, upload_to=apps.common.utils.generate_upload_path, validators=[apps.common.validators.file_size], verbose_name='Ikonka'),
        ),
        # Skip AlterField operations for slug fields - we use constraints instead of unique=True
    ]
