from django.core.management.base import BaseCommand
import cloudinary
import cloudinary.api
from django.conf import settings
import json

class Command(BaseCommand):
    help = 'Check what media files are stored in Cloudinary'

    def handle(self, *args, **options):
        self.stdout.write('Checking Cloudinary storage...')
        
        try:
            # Get resources from Cloudinary
            result = cloudinary.api.resources(
                resource_type="image",
                max_results=30,
                type="upload"
            )
            
            # Display resources
            self.stdout.write('Found the following files in Cloudinary:')
            self.stdout.write('-' * 60)
            
            if 'resources' in result and result['resources']:
                for resource in result['resources']:
                    self.stdout.write(f"File: {resource['public_id']}")
                    self.stdout.write(f"URL: {resource['secure_url']}")
                    self.stdout.write(f"Size: {resource['bytes']/1024:.2f} KB")
                    self.stdout.write(f"Created: {resource['created_at']}")
                    self.stdout.write('-' * 60)
                
                self.stdout.write(self.style.SUCCESS(
                    f"Found {len(result['resources'])} files in your Cloudinary account."
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    "No files found in your Cloudinary account."
                ))
                
            # Show usage information
            usage = cloudinary.api.usage()
            self.stdout.write("\nCloudinary Account Usage:")
            
            # Fix for the usage reporting structure
            if isinstance(usage.get('transformations'), dict):
                self.stdout.write(f"Transformations: {usage['transformations'].get('usage', 0)}")
            else:
                self.stdout.write(f"Transformations: {usage.get('transformations', 0)}")
                
            if isinstance(usage.get('objects'), dict):
                self.stdout.write(f"Objects: {usage['objects'].get('usage', 0)}")
            else:
                self.stdout.write(f"Objects: {usage.get('objects', 0)}")
                
            if isinstance(usage.get('bandwidth'), dict):
                bandwidth_mb = usage['bandwidth'].get('usage', 0) / 1024 / 1024
            else:
                bandwidth_mb = usage.get('bandwidth', 0) / 1024 / 1024
            self.stdout.write(f"Bandwidth: {bandwidth_mb:.2f} MB")
            
            if isinstance(usage.get('storage'), dict):
                storage_mb = usage['storage'].get('usage', 0) / 1024 / 1024
            else:
                storage_mb = usage.get('storage', 0) / 1024 / 1024
            self.stdout.write(f"Storage: {storage_mb:.2f} MB")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"Error checking Cloudinary: {str(e)}"
            ))
