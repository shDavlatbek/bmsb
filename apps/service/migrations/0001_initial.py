# Generated by Django 5.2.1 on 2025-07-03 07:10

import apps.common.mixins
import apps.common.utils
import apps.common.validators
import django.db.models.deletion
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0037_alter_contactform_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sana')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan sana")),
                ('is_active', models.BooleanField(default=True, verbose_name='Faoligi')),
                ('name', models.CharField(max_length=255, verbose_name='Nomi')),
                ('name_uz', models.CharField(max_length=255, null=True, verbose_name='Nomi')),
                ('name_ru', models.CharField(max_length=255, null=True, verbose_name='Nomi')),
                ('name_en', models.CharField(max_length=255, null=True, verbose_name='Nomi')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('description', tinymce.models.HTMLField(verbose_name='Tavsifi')),
                ('description_uz', tinymce.models.HTMLField(null=True, verbose_name='Tavsifi')),
                ('description_ru', tinymce.models.HTMLField(null=True, verbose_name='Tavsifi')),
                ('description_en', tinymce.models.HTMLField(null=True, verbose_name='Tavsifi')),
                ('tags', models.CharField(blank=True, help_text='Taglarni probel bilan ajrating', max_length=255, null=True, verbose_name='Taglar')),
                ('tags_uz', models.CharField(blank=True, help_text='Taglarni probel bilan ajrating', max_length=255, null=True, verbose_name='Taglar')),
                ('tags_ru', models.CharField(blank=True, help_text='Taglarni probel bilan ajrating', max_length=255, null=True, verbose_name='Taglar')),
                ('tags_en', models.CharField(blank=True, help_text='Taglarni probel bilan ajrating', max_length=255, null=True, verbose_name='Taglar')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='services', to='main.school', verbose_name='Maktab')),
            ],
            options={
                'verbose_name': 'Xizmat',
                'verbose_name_plural': 'Xizmatlar',
            },
            bases=(apps.common.mixins.SlugifyMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CultureArt',
            fields=[
                ('service_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='service.service')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('phone_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='Telefon raqami')),
                ('author_image', models.ImageField(blank=True, help_text="Rasm 5 MB dan katta bo'lishi mumkin emas.", null=True, upload_to=apps.common.utils.generate_upload_path, validators=[apps.common.validators.file_size], verbose_name='Muallif rasmi')),
                ('author_name', models.CharField(max_length=255, verbose_name='Muallif ismi')),
                ('author_name_uz', models.CharField(max_length=255, null=True, verbose_name='Muallif ismi')),
                ('author_name_ru', models.CharField(max_length=255, null=True, verbose_name='Muallif ismi')),
                ('author_name_en', models.CharField(max_length=255, null=True, verbose_name='Muallif ismi')),
                ('author_musical_instrument', models.CharField(blank=True, max_length=255, null=True, verbose_name='Muallif musiqaviy instrumenti')),
                ('author_musical_instrument_uz', models.CharField(blank=True, max_length=255, null=True, verbose_name='Muallif musiqaviy instrumenti')),
                ('author_musical_instrument_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name='Muallif musiqaviy instrumenti')),
                ('author_musical_instrument_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Muallif musiqaviy instrumenti')),
                ('author_direction', models.CharField(blank=True, max_length=255, null=True, verbose_name="Muallif yo'nalishi")),
                ('author_direction_uz', models.CharField(blank=True, max_length=255, null=True, verbose_name="Muallif yo'nalishi")),
                ('author_direction_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name="Muallif yo'nalishi")),
                ('author_direction_en', models.CharField(blank=True, max_length=255, null=True, verbose_name="Muallif yo'nalishi")),
                ('author_honor', models.CharField(blank=True, max_length=255, null=True, verbose_name='Muallif yutuqlari')),
                ('author_honor_uz', models.CharField(blank=True, max_length=255, null=True, verbose_name='Muallif yutuqlari')),
                ('author_honor_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name='Muallif yutuqlari')),
                ('author_honor_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Muallif yutuqlari')),
            ],
            options={
                'verbose_name': "Madaniy san'at",
                'verbose_name_plural': "Madaniy san'atlar",
            },
            bases=('service.service',),
        ),
        migrations.CreateModel(
            name='CultureService',
            fields=[
                ('service_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='service.service')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Narxi')),
            ],
            options={
                'verbose_name': 'Madaniy xizmat',
                'verbose_name_plural': 'Madaniy xizmatlar',
            },
            bases=('service.service',),
        ),
        migrations.CreateModel(
            name='FineArt',
            fields=[
                ('service_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='service.service')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('phone_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='Telefon raqami')),
                ('author_image', models.ImageField(blank=True, help_text="Rasm 5 MB dan katta bo'lishi mumkin emas.", null=True, upload_to=apps.common.utils.generate_upload_path, validators=[apps.common.validators.file_size], verbose_name='Muallif rasmi')),
                ('author_name', models.CharField(max_length=255, verbose_name='Muallif ismi')),
                ('author_name_uz', models.CharField(max_length=255, null=True, verbose_name='Muallif ismi')),
                ('author_name_ru', models.CharField(max_length=255, null=True, verbose_name='Muallif ismi')),
                ('author_name_en', models.CharField(max_length=255, null=True, verbose_name='Muallif ismi')),
                ('author_musical_instrument', models.CharField(blank=True, max_length=255, null=True, verbose_name='Muallif musiqaviy instrumenti')),
                ('author_musical_instrument_uz', models.CharField(blank=True, max_length=255, null=True, verbose_name='Muallif musiqaviy instrumenti')),
                ('author_musical_instrument_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name='Muallif musiqaviy instrumenti')),
                ('author_musical_instrument_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Muallif musiqaviy instrumenti')),
                ('author_direction', models.CharField(blank=True, max_length=255, null=True, verbose_name="Muallif yo'nalishi")),
                ('author_direction_uz', models.CharField(blank=True, max_length=255, null=True, verbose_name="Muallif yo'nalishi")),
                ('author_direction_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name="Muallif yo'nalishi")),
                ('author_direction_en', models.CharField(blank=True, max_length=255, null=True, verbose_name="Muallif yo'nalishi")),
                ('author_honor', models.CharField(blank=True, max_length=255, null=True, verbose_name='Muallif yutuqlari')),
                ('author_honor_uz', models.CharField(blank=True, max_length=255, null=True, verbose_name='Muallif yutuqlari')),
                ('author_honor_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name='Muallif yutuqlari')),
                ('author_honor_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Muallif yutuqlari')),
            ],
            options={
                'verbose_name': "Tasviriy san'at",
                'verbose_name_plural': "Tasviriy san'atlar",
            },
            bases=('service.service',),
        ),
        migrations.CreateModel(
            name='ServiceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sana')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan sana")),
                ('is_active', models.BooleanField(default=True, verbose_name='Faoligi')),
                ('image', models.ImageField(help_text="Rasm 5 MB dan katta bo'lishi mumkin emas.", upload_to=apps.common.utils.generate_upload_path, validators=[apps.common.validators.file_size], verbose_name='Rasm')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_images', to='service.service', verbose_name='Xizmat')),
            ],
            options={
                'verbose_name': 'Xizmat rasmi',
                'verbose_name_plural': 'Xizmat rasmlari',
            },
        ),
        migrations.CreateModel(
            name='CultureServiceFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sana')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan sana")),
                ('is_active', models.BooleanField(default=True, verbose_name='Faoligi')),
                ('file', models.FileField(help_text="Fayl 5 MB dan katta bo'lishi mumkin emas.", upload_to=apps.common.utils.generate_upload_path, validators=[apps.common.validators.file_size], verbose_name='Fayl')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_files', to='service.cultureservice', verbose_name='Xizmat')),
            ],
            options={
                'verbose_name': 'Xizmat fayli',
                'verbose_name_plural': 'Xizmat fayllari',
            },
        ),
        migrations.AddConstraint(
            model_name='service',
            constraint=models.UniqueConstraint(fields=('school', 'slug'), name='unique_service_school_slug'),
        ),
    ]
