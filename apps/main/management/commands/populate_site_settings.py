from django.core.management.base import BaseCommand
from apps.main.models import School, SiteSettings


class Command(BaseCommand):
    help = 'Create default SiteSettings for schools that don\'t have them (safe for production)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--school-id',
            type=int,
            help='Create SiteSettings for a specific school ID',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Update existing SiteSettings with default values (use with caution)',
        )

    def handle(self, *args, **options):
        school_id = options.get('school_id')
        dry_run = options.get('dry_run')
        force = options.get('force')
        
        # Define default SiteSettings values
        default_settings = {
            'school_life': "Maktabimiz hayoti haqida ma'lumot",
            'directions': "Bizning yo'nalishlar haqida ma'lumot",
            'numbers': "Maktab raqamlari haqida ma'lumot",
            'teachers': "O'qituvchilarimiz haqida ma'lumot",
            'honors': "Maktabimiz faxrlari haqida ma'lumot",
            'news': "Yangiliklar bo'limi haqida ma'lumot",
            'gallery': "Galereya bo'limi haqida ma'lumot",
            'contact': "Bog'lanish bo'limi haqida ma'lumot",
            'comments': "Izohlar bo'limi haqida ma'lumot",
            'faqs': "Ko'p beriladigan savollar haqida ma'lumot",
            'leaders': "Rahbariyat bo'limi haqida ma'lumot",
            'vacancies': "Vakansiyalar bo'limi haqida ma'lumot",
            'documents': "Hujjatlar bo'limi haqida ma'lumot",
            'timetables': "O'quv reja bo'limi haqida ma'lumot",
            'edu_infos': "Ta'lim ma'lumotlari bo'limi haqida ma'lumot",
            'events': "Tadbirlar bo'limi haqida ma'lumot",
            'resources': "Resurslar bo'limi haqida ma'lumot",
            'culture_services': "Madaniy xizmatlar haqida ma'lumot",
            'culture_arts': "Madaniy san'at haqida ma'lumot",
            'fine_arts': "Tasviriy san'at haqida ma'lumot"
        }
        
        if school_id:
            # Process specific school
            try:
                schools = [School.objects.get(id=school_id)]
                self.stdout.write(f"Processing specific school: {schools[0].name} (ID: {school_id})")
            except School.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'School with ID {school_id} does not exist.')
                )
                return
        else:
            # Process all schools
            schools = School.objects.all()
            self.stdout.write(f"Processing all schools ({schools.count()} found)")
        
        if not schools:
            self.stdout.write(self.style.WARNING('No schools found.'))
            return
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        
        for school in schools:
            try:
                # Check if SiteSettings already exists
                existing_settings = SiteSettings.objects.filter(school=school).first()
                
                if existing_settings and not force:
                    self.stdout.write(
                        self.style.WARNING(f'→ {school.name}: SiteSettings already exists (ID: {existing_settings.id}) - skipped')
                    )
                    skipped_count += 1
                    continue
                
                if dry_run:
                    if existing_settings and force:
                        self.stdout.write(
                            self.style.WARNING(f'[DRY RUN] Would update SiteSettings for: {school.name}')
                        )
                        updated_count += 1
                    else:
                        self.stdout.write(
                            self.style.SUCCESS(f'[DRY RUN] Would create SiteSettings for: {school.name}')
                        )
                        created_count += 1
                    continue
                
                if existing_settings and force:
                    # Update existing settings
                    for field, value in default_settings.items():
                        if not getattr(existing_settings, field):  # Only update empty fields
                            setattr(existing_settings, field, value)
                    existing_settings.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'✔ {school.name}: Updated existing SiteSettings (ID: {existing_settings.id})')
                    )
                    updated_count += 1
                else:
                    # Create new settings
                    site_settings = SiteSettings.objects.create(
                        school=school,
                        **default_settings
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'✔ {school.name}: Created SiteSettings (ID: {site_settings.id})')
                    )
                    created_count += 1
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ {school.name}: Error - {str(e)}')
                )
        
        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== SUMMARY ==='))
        if dry_run:
            self.stdout.write(f'Would create: {created_count}')
            self.stdout.write(f'Would update: {updated_count}')
        else:
            self.stdout.write(f'Created: {created_count}')
            self.stdout.write(f'Updated: {updated_count}')
        self.stdout.write(f'Skipped: {skipped_count}')
        self.stdout.write(f'Total schools processed: {len(schools)}')
        
        if dry_run:
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('This was a dry run. No changes were made.'))
            self.stdout.write('Run without --dry-run to apply changes.')
        else:
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('✅ Operation completed successfully!')) 