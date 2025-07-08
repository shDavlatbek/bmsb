from django.core.management.base import BaseCommand
from apps.main.models import School, TimeTable


class Command(BaseCommand):
    help = 'Add default timetables for schools that don\'t have them'

    def add_arguments(self, parser):
        parser.add_argument(
            '--school-id',
            type=int,
            help='Add timetables for a specific school ID',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating',
        )

    def handle(self, *args, **options):
        school_id = options.get('school_id')
        dry_run = options.get('dry_run')
        
        # Define the default timetables structure
        time_tables = [
            {'uz': '1-sinflar', 'ru': '1-классы', 'en': '1-classes'},
            {'uz': '2-sinflar', 'ru': '2-классы', 'en': '2-classes'},
            {'uz': '3-sinflar', 'ru': '3-классы', 'en': '3-classes'},
            {'uz': '4-sinflar', 'ru': '4-классы', 'en': '4-classes'},
            {'uz': '5-sinflar', 'ru': '5-классы', 'en': '5-classes'},
            {'uz': '6-sinflar', 'ru': '6-классы', 'en': '6-classes'},
            {'uz': '7-sinflar', 'ru': '7-классы', 'en': '7-classes'},
            {'uz': '8-sinflar', 'ru': '8-классы', 'en': '8-classes'},
            {'uz': '9-sinflar', 'ru': '9-классы', 'en': '9-classes'},
        ]
        
        if school_id:
            # Process specific school
            try:
                schools = [School.objects.get(id=school_id)]
                self.stdout.write(f"Processing school ID: {school_id}")
            except School.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'School with ID {school_id} does not exist.')
                )
                return
        else:
            # Get all schools
            schools = School.objects.all()
            self.stdout.write(f"Processing {schools.count()} schools")
        
        schools_processed = 0
        timetables_created = 0
        
        for school in schools:
            # Check if school already has timetables
            existing_timetables = TimeTable.objects.filter(school=school).count()
            
            if existing_timetables == 0:
                schools_processed += 1
                
                if dry_run:
                    self.stdout.write(
                        f"[DRY RUN] Would create {len(time_tables)} timetables for school: {school.name} (ID: {school.id})"
                    )
                    timetables_created += len(time_tables)
                else:
                    # Create timetables for this school
                    for time_table in time_tables:
                        TimeTable.objects.create(
                            school=school,
                            title=time_table['uz'],
                            title_uz=time_table['uz'],
                            title_ru=time_table['ru'],
                            title_en=time_table['en']
                        )
                        timetables_created += 1
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created {len(time_tables)} timetables for school: {school.name} (ID: {school.id})"
                        )
                    )
            else:
                self.stdout.write(
                    f"School '{school.name}' (ID: {school.id}) already has {existing_timetables} timetables. Skipping."
                )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"\n[DRY RUN COMPLETE] Would have processed {schools_processed} schools "
                    f"and created {timetables_created} timetables."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nCompleted! Processed {schools_processed} schools "
                    f"and created {timetables_created} timetables."
                )
            ) 