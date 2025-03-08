from django.core.management.base import BaseCommand
import cloudinary
import cloudinary.uploader
import os
from django.conf import settings
from main.models import Project

class Command(BaseCommand):
    help = 'Migrate all project images from local storage to Cloudinary'

    def handle(self, *args, **options):
        self.stdout.write('Starting migration of project images to Cloudinary...')
        
        # Get all projects
        projects = Project.objects.all()
        migrated_count = 0
        
        for project in projects:
            if not project.image:
                self.stdout.write(f"Project '{project.title}' has no image, skipping.")
                continue
                
            # Get image path
            if isinstance(project.image, str):
                # Handle case where image might be already a URL
                image_path = project.image
                is_local_file = False
                self.stdout.write(f"Project '{project.title}' has image URL: {image_path}")
            else:
                # Handle case where image is a file field
                image_path = os.path.join(settings.MEDIA_ROOT, str(project.image))
                is_local_file = os.path.exists(image_path)
                self.stdout.write(f"Project '{project.title}' has image path: {image_path}")
            
            try:
                if is_local_file:
                    # Upload to Cloudinary
                    self.stdout.write(f"Uploading {image_path} to Cloudinary...")
                    result = cloudinary.uploader.upload(
                        image_path,
                        folder="projects",
                        public_id=os.path.splitext(os.path.basename(image_path))[0]
                    )
                    
                    # Update project with Cloudinary image
                    project.image = result['public_id']
                    project.save()
                    
                    self.stdout.write(self.style.SUCCESS(
                        f"Migrated image for '{project.title}': {result['secure_url']}"
                    ))
                    migrated_count += 1
                else:
                    self.stdout.write(self.style.WARNING(
                        f"Could not find local file for '{project.title}'"
                    ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Error migrating image for '{project.title}': {str(e)}"
                ))
                
        self.stdout.write(self.style.SUCCESS(
            f"Migration complete. {migrated_count} of {projects.count()} project images migrated."
        ))
