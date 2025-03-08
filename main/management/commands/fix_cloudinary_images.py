from django.core.management.base import BaseCommand
import cloudinary
import cloudinary.uploader
from django.conf import settings
from main.models import Project
import logging
import os

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Check and fix Cloudinary image URLs in projects'

    def handle(self, *args, **options):
        self.stdout.write('Checking project images in Cloudinary...')
        
        projects = Project.objects.all()
        self.stdout.write(f"Found {projects.count()} projects.")
        
        for i, project in enumerate(projects, 1):
            self.stdout.write(f"[{i}/{projects.count()}] Checking project: {project.title}")
            
            # Skip if no image
            if not project.image:
                self.stdout.write(f"  - No image for project {project.id}")
                continue
            
            try:
                # Try to access image URL (this will trigger an error if something is wrong)
                image_url = project.image.url
                self.stdout.write(f"  - Image URL is valid: {image_url}")
                
                # Verify that image exists in Cloudinary
                try:
                    # Get public_id if available
                    public_id = getattr(project.image, 'public_id', None)
                    if public_id:
                        cloudinary.api.resource(public_id)
                        self.stdout.write(f"  - Image exists in Cloudinary with public_id: {public_id}")
                    else:
                        self.stdout.write(f"  - Cannot verify image in Cloudinary (no public_id)")
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"  - Cannot verify image in Cloudinary: {str(e)}"))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  - Error accessing image for project {project.id}: {str(e)}"))
                
                # If we have a default project image, try to upload it to Cloudinary as a fix
                default_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'default-project.jpeg')
                
                if os.path.exists(default_image_path):
                    try:
                        self.stdout.write("  - Uploading default image as fix...")
                        result = cloudinary.uploader.upload(
                            default_image_path,
                            folder="projects",
                            public_id=f"fixed_project_{project.id}"
                        )
                        
                        # Update the project's image field
                        project.image = result['public_id']
                        project.save()
                        
                        self.stdout.write(self.style.SUCCESS(
                            f"  - Fixed project image: {result['secure_url']}"
                        ))
                    except Exception as upload_error:
                        self.stdout.write(self.style.ERROR(f"  - Failed to fix image: {str(upload_error)}"))
                else:
                    self.stdout.write(self.style.ERROR(f"  - Default image not found at: {default_image_path}"))
                    
        self.stdout.write(self.style.SUCCESS(f"Finished checking {projects.count()} projects"))
