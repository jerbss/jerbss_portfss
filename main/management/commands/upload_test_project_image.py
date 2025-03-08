from django.core.management.base import BaseCommand
import cloudinary
import cloudinary.uploader
import os
from django.conf import settings
from main.models import Project
import glob

class Command(BaseCommand):
    help = 'Upload an existing project image to Cloudinary for testing'

    def handle(self, *args, **options):
        self.stdout.write('Testing upload of project images to Cloudinary...')
        
        try:
            # First check - try to find a project with an image
            projects = Project.objects.filter(image__isnull=False)
            
            if projects.exists():
                # Get the first project with an image
                project = projects.first()
                self.stdout.write(f"Found project with image: {project.title}")
                
                # Get local file path
                local_path = os.path.join(settings.MEDIA_ROOT, str(project.image))
                
                if os.path.exists(local_path):
                    self.stdout.write(f"Image file exists at: {local_path}")
                    
                    # Upload directly to Cloudinary
                    result = cloudinary.uploader.upload(
                        local_path,
                        folder="projects_test",
                        public_id=f"test_{os.path.basename(project.image.name)}"
                    )
                    
                    self.stdout.write(self.style.SUCCESS(
                        f"Successfully uploaded to Cloudinary at: {result['secure_url']}"
                    ))
                else:
                    self.stdout.write(self.style.WARNING(f"File not found: {local_path}"))
                    
                    # Try to find any image files in the media folder
                    media_images = glob.glob(os.path.join(settings.MEDIA_ROOT, 'projects', '*.jpg')) + \
                                  glob.glob(os.path.join(settings.MEDIA_ROOT, 'projects', '*.png')) + \
                                  glob.glob(os.path.join(settings.MEDIA_ROOT, 'projects', '*.jpeg'))
                    
                    if media_images:
                        # Try the first found image
                        test_image = media_images[0]
                        self.stdout.write(f"Found alternative image to test: {test_image}")
                        
                        result = cloudinary.uploader.upload(
                            test_image,
                            folder="projects_test",
                            public_id=f"test_{os.path.basename(test_image)}"
                        )
                        
                        self.stdout.write(self.style.SUCCESS(
                            f"Successfully uploaded to Cloudinary at: {result['secure_url']}"
                        ))
                    else:
                        self.stdout.write(self.style.ERROR("No image files found in media folder"))
            else:
                self.stdout.write(self.style.WARNING("No projects with images found in database"))
                
                # Try to find any image files in the media folder
                media_images = glob.glob(os.path.join(settings.MEDIA_ROOT, 'projects', '*.jpg')) + \
                              glob.glob(os.path.join(settings.MEDIA_ROOT, 'projects', '*.png')) + \
                              glob.glob(os.path.join(settings.MEDIA_ROOT, 'projects', '*.jpeg'))
                
                if media_images:
                    # Try the first found image
                    test_image = media_images[0]
                    self.stdout.write(f"Found image to test: {test_image}")
                    
                    result = cloudinary.uploader.upload(
                        test_image,
                        folder="projects_test",
                        public_id=f"test_{os.path.basename(test_image)}"
                    )
                    
                    self.stdout.write(self.style.SUCCESS(
                        f"Successfully uploaded to Cloudinary at: {result['secure_url']}"
                    ))
                else:
                    self.stdout.write(self.style.ERROR("No image files found in media folder"))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"Error during test upload: {str(e)}"
            ))
