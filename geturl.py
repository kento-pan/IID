import requests
insta_link = "https://www.instagram.com/p/"

def photo_id(user_input):
	insta_pic_url = insta_link + user_input
	r = requests.get(insta_pic_url)
	global r_text
	r_text = r.text
