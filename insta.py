import requests, shutil, os, platform, getpass
from bs4 import BeautifulSoup
from PIL import Image, ImageFile

# OS and path
os_platform = platform.system()
new_folder = "Instagram Downloads/"

if os_platform == "Windows":
    username = os.environ["username"]
    path = "C:\\Users\\" + username + "\\Downloads\\"
elif os_platform == "Darwin":
    username = getpass.getuser()
    path = "/Users/" + username + "/Downloads/"
elif os_platform =='Linux':
    username=getpass.getuser()
    path = "/home/"+username+"/Downloads/"
else:
	print("Sorry, OS not supported. Closing script.")
	quit()
save_to = path + new_folder

if os.path.isdir(save_to) == False:
    os.mkdir(path + new_folder)
    print("Created new target folder.")
else:
    print("Target folder exists already.")

# Get the link
insta_link = "https://www.instagram.com/p/"
photo_id = input("Please copy and paste the Instagram photo ID from the URL: ")

insta_pic_url = insta_link + photo_id

r = requests.get(insta_pic_url)
r_text = r.text

# Parse the page
html_parser = BeautifulSoup(r_text, features='html.parser')
find_og_image = html_parser.find("meta", property="og:image")

if find_og_image == None:
	print("No image found. Please verify the photo ID or link.")
	quit()
else:
	og_image_link = find_og_image["content"]

# Download the image
r_og_image = requests.get(og_image_link, stream=True)

if os.path.exists(save_to + photo_id + ".jpg") == False:
    local_file = open(save_to + photo_id + ".jpg", "x+b")
else:
    print("File exists already. Download cancelled.")
    quit()

#r_og_image.raw.decode_content = True

shutil.copyfileobj(r_og_image.raw, local_file)

#del r_og_image

print("Image downloaded and saved to " + save_to)

# Open the image
ImageFile.LOAD_TRUNCATED_IMAGES = True

image = Image.open(save_to + photo_id + ".jpg")

image.show()
