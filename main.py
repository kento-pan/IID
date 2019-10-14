import os
import requests
import shutil
import geturl
from pathlib import Path
from bs4 import BeautifulSoup
#  from PIL import Image, ImageFile // Not used for now.

print("###########################################")
print("##                                       ##")
print("##       Instagram Image Downloader      ##")
print("##                  by                   ##")
print("##              kento pan                ##")
print("##                                       ##")
print("###########################################")
print()
print()

# OS and path: We need to save the downloaded files somewhere. Here we create
# a new folder for our downloads and choose a fitting directory.

new_folder = "/Instagram Downloads/"
path = Path.home() / "Downloads"
save_to = str(path) + new_folder

print(f"Checking system for existing {new_folder} folder in {path}.")
if not os.path.isdir(save_to):
    os.mkdir(str(path) + new_folder)
    print(f"{new_folder} not found. Created new target folder.")
else:
    print(f"Target folder {new_folder} exists already.")

print("Enter each Instagram photo ID separetely and press ENTER to confirm.")
print("Press ENTER again, without any input to start downloading.")

# Get the photo IDs: We ask the user to give us the photo IDs
# and store them in a list.

photo_id_list = []  # List to store photo IDs.

while True:
    photo_id_list.append(str.strip(
        input("Please enter the Instagram photo ID from the URL here: ")))
    if photo_id_list[-1] == "":
        photo_id_list.remove("")  # Removes the last empty string
        # from the list.
        print(f"No Input detected. Starting downloads.")
        break  # Stops asking for Inputs.

r_og_image = ""
og_image_link = ""
photo = ""

# Process the input: Now we are looping through the list of ID, parse
# the webpage and download the image.

for i in photo_id_list:
    geturl.photo_id(i)  # geturl function from geturl.py and
    # the requests module are used to load the page.

    # Parse the page: BeautifulSoup is used to parse the page and find
    # the original photo from it.
    html_parser = BeautifulSoup(geturl.r_text, features='html.parser')
    find_og_image = html_parser.find("meta", property="og:image")

    if find_og_image is None:  # Verfies if an image is found.
        print(f"No image found for '{i}'. Please verify the photo ID.")
        break
    else:
        og_image_link = find_og_image["content"]

    # Download the image: We use requests again to download the image and
    # save it to our predefined directory.
    r_og_image = requests.get(og_image_link, stream=True)

    photo = f"{save_to}{i}.jpg"

    if not os.path.exists(photo):
        with open(photo, "x+b") as local_file:
            shutil.copyfileobj(r_og_image.raw, local_file)
            print(f"{i}.jpg downloaded and saved to {save_to}.")
    else:
        print(f"{i}.jpg exists already. Download skipped.")

print(f"Done. All new images saved to {save_to}.")
# Open the image. // Not used for now.
# ImageFile.LOAD_TRUNCATED_IMAGES = True
# image = Image.open(photo)
# image.show()
