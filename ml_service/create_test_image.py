from PIL import Image, ImageDraw

# Create a new image with a white background
image = Image.new('RGB', (100, 100), 'white')

# Get a drawing context
draw = ImageDraw.Draw(image)

# Draw something (a simple rectangle)
draw.rectangle([30, 30, 70, 70], fill='blue')

# Save the image
image.save('test_images/test_image.jpg')
