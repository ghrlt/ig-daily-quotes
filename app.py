import os
import json
import time
import requests
import textwrap

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

import instagrapi

from dotenv import load_dotenv
load_dotenv()

import logging

# Silence other loggers
for log_name, log_obj in logging.Logger.manager.loggerDict.items():
	 if log_name != __name__:
		  log_obj.disabled = True

logging.basicConfig(
	format='%(asctime)s %(levelname)-8s %(message)s',
	level=logging.DEBUG,
	datefmt='%Y-%m-%d %H:%M:%S'
)


username = os.getenv('ig-username') or input("Instagram username? ")
password = os.getenv('ig-password') or input("Instagram password? ")

session_file = f"{username}.session"


BOT = instagrapi.Client()

if session_file in os.listdir():
	BOT.load_settings(session_file)

BOT.login(username, password)
logging.info("Logged in")

BOT.dump_settings(session_file)



QUOTE_FONT = ImageFont.truetype("Raleway-SemiBold.ttf", 80)
AUTHOR_FONT = ImageFont.truetype("Raleway-Medium.ttf", 46)


def get_quote():
	r = requests.get(
		"https://api.quotable.io/random",
		params={"maxLength": 80, "tags": "famous-quotes"}
	).json()

	if '.posted' in os.listdir():
		with open('.posted', 'r') as f:
			posted = json.load(f)
	else:
		posted = {}

	if posted.get(r['_id']):
		logging.debug("Quote %s already posted. Fetching another", r['_id'])
		return task()

	posted[r['_id']] = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")

	with open('.posted', 'w') as f:
		json.dump(posted, f, indent=1)

	qid = r['_id']
	quote = r['content']
	author = r['author']
	return qid, quote, author

def get_hashtags():
	hashtags = [
		'quote', 'quotes', 'pic', 'picoftheday', 'dailypic', 'quoteporn', 'quotesporn', 'models',
		'instagram', 'trending', 'love', 'explore', 'fashion', 'tiktok', 'likeforlikes',
		'photography', 'trend', 'instadaily', 'music', 'trendingnow', 'foryou', 'photooftheday',
		'bhfyp', 'viralpost'
	]
	# Too muche time for nothing
	#for hashtag in hashtags:
	#	try:
	#		hashtags += BOT.hashtag_related_hashtags(hashtag)
	#	except:
	#		pass


	return ' '.join([f"#{hashtag}" for hashtag in hashtags])

def get_media(qid, quote, author):
	quote_lines = textwrap.wrap(quote, width=20)

	img = Image.new("RGB", (1080, 1080), color=(27,27,27))
	draw = ImageDraw.Draw(img)

	atw, ath = AUTHOR_FONT.getsize(author)
	apos = ((1080-atw-ath*2), (1080-ath*2-15))

	QDIVH = apos[1]-(1080-apos[1])


	q_startpos = 1080-QDIVH
	q_linepadding = 50
	h = q_startpos

	for i,line in enumerate(quote_lines):
		qltw, qlth = QUOTE_FONT.getsize(line)

		pos = ((1080-qltw)/2, h)
		h += qlth + q_linepadding
		
		draw.text(pos, line, fill="white", font=QUOTE_FONT)

	draw.text(apos, author, fill="white", font=AUTHOR_FONT)

	path = f"temppic-{qid}.jpg"
	img.save(path, "JPEG")

	return path


def task():
	# Obtain quote
	qid, quote, author = get_quote()

	# Obtain trending hashtags
	hashtags = get_hashtags()

	# Generate media
	path = get_media(qid, quote, author)

	# Upload media
	BOT.photo_upload(path, f"✔ Follow 💌 Comment 🛐 Share\n\nToday's quote is from {author}\n\nHashtags (don't mind them):\n{hashtags}")

	# Deleting local media file
	os.remove(path)


schedule.every().day.at("16:30").do(task)

while 1:
	schedule.run_pending()
	time.sleep(60)