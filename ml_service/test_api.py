import requests

# API endpoint
url = 'http://localhost:8080/predict'

# Test with a sample image file
try:
    with open('test_images/test_image.jpg', 'rb') as f:
        files = {'file': ('test_image.jpg', f, 'image/jpeg')}
        response = requests.post(url, files=files)
        
        if response.status_code == 200:
            print("Success!")
            print("Response:", response.json())
        else:
            print(f"Error: Status code {response.status_code}")
            print("Response:", response.text)
except FileNotFoundError:
    print("Please make sure test_image.jpg exists in the current directory")
except Exception as e:
    print(f"Error: {str(e)}")
