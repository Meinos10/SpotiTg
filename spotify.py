# Developer: https://t.me/ReWoxi

from email import message
import spotipy
from config import *
from spotipy.oauth2 import SpotifyOAuth
from pyrogram import Client
from pyrogram.types import InputMediaPhoto
from pyrogram.errors import MessageNotModified
import time
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


Bot = Client(
    "Spotify",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=token
)

def button(name, url):
    BUTTON = [[InlineKeyboardButton(f"Open Spotify: {name} ✨", url=url)]]
    return InlineKeyboardMarkup(BUTTON)

with Bot as client:
	try:
		sp = spotipy.Spotify(
			auth_manager=SpotifyOAuth(
				client_id=SPOTIPY_CLIENT_ID,
				client_secret=SPOTIPY_CLIENT_SECRET,
				redirect_uri=SPOTIPY_REDIRECT_URI,
				scope=SCOPE
		))
		print("Bağlandı!")
	except Exception as e:
		print(e)

	user = sp.current_user()
	#client.send_photo(chat, photo=user["images"][0]["url"], caption="**User Spotify Name: `{}`\nTotal Followers: `{}`**".format(user["display_name"], user["followers"]["total"]))
	current_song = ""
	while True:
		music = sp.currently_playing(MARKET)
		if not music["is_playing"]:
			print("Play Music: OFF")
			exit()
		else:
			if current_song == music["item"]["artists"][0]["name"] + " - " + music["item"]["name"]:
				pass
			else:
				current_song = music["item"]["artists"][0]["name"] + " - " + music["item"]["name"]
				try:
					client.edit_message_media(
						chat,
						message_id=msg_id,
						media=InputMediaPhoto(music["item"]["album"]["images"][1]["url"])
					)
				except MessageNotModified:
					pass
				try:
					client.edit_message_text(
						chat, 
						message_id=msg_id,
						text="**Şuan Çalan!\n\nSanatcı: `{}`\n\nMüzik: `{}` 🎶\n\n**".format(music["item"]["artists"][0]["name"], music["item"]["name"]),
						reply_markup=button(music["item"]["name"], music["item"]["external_urls"]["spotify"]))
				except MessageNotModified as e:
					pass
			time.sleep(10)
