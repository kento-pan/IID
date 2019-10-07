import os
import requests
import shutil
import geturl
from PIL import Image, ImageFile
from pathlib import Path
from bs4 import BeautifulSoup

# OS and path: We need to save the downloaded files somewhere. Here we create a new folder for our downloads
# and choose a fitting directory.

new_folder = "/Instagram Downloads/"

path = Path.home() / "Downloads"
save_to = str(path) + new_folder

if not os.path.isdir(save_to):
    os.mkdir(str(path) + new_folder)
    print("Created new target folder.")
else:
    print("Target folder exists already.")

# Get the link: We ask the user to give us the photo id, which we use to create the URL and the filename.
# With requests with load the page.
user_input = input("Please copy and paste the Instagram photo ID from the URL: ")
geturl.photo_id(user_input)

# Parse the page: BeautifulSoup is used to parse the page and find the original photo from it.
html_parser = BeautifulSoup(geturl.r_text, features='html.parser')
find_og_image = html_parser.find("meta", property="og:image")

if find_og_image is None:
    print(f"No image found. Please verify the photo ID.")
    quit()
else:
    og_image_link = find_og_image["content"]

# Download the image: We use requests again to download the image and save it to our predefined directory.
r_og_image = requests.get(og_image_link, stream=True)

photo = f"{save_to}{user_input}.jpg"

if not os.path.exists(photo):
    with open(photo, "x+b") as local_file:
        shutil.copyfileobj(r_og_image.raw, local_file)
else:
    print("File exists already. Download cancelled.")
    quit()

print(f"Image downloaded and saved to {save_to} as {user_input}.jpg")

# Open the image
ImageFile.LOAD_TRUNCATED_IMAGES = True
image = Image.open(photo)
image.show()
