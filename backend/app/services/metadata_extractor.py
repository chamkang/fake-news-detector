import exifread
from io import BytesIO
from PIL import Image
import os

class MetadataExtractor:
    def __init__(self):
        self.interesting_tags = [
            'Image DateTime',
            'Image Make',
            'Image Model',
            'Image Software',
            'EXIF DateTimeOriginal',
            'EXIF DateTimeDigitized',
            'EXIF ISOSpeedRatings',
            'EXIF ExposureTime',
            'EXIF FNumber',
            'EXIF ExposureProgram',
            'EXIF ExifVersion'
        ]

    def extract(self, image_data):
        """Extract metadata from image"""
        try:
            metadata = {}
            
            # Read EXIF data
            tags = exifread.process_file(BytesIO(image_data))
            
            # Extract interesting EXIF tags
            for tag in self.interesting_tags:
                if tag in tags:
                    metadata[tag.split()[-1]] = str(tags[tag])
            
            # Get basic image info using PIL
            with Image.open(BytesIO(image_data)) as img:
                metadata.update({
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                })
            
            return metadata
            
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            return {}
