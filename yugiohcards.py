language="English" #changing this will have undefined results

import os, sys
import sqlite3
from urllib.request import urlretrieve

def card_info(card):
	card_level=card["level"] & 0xff
	types=[]
	final={}
	display_string=""
	final["types"]="None"
	final["attributes"]="None"
	final["races"]="None"
	for i in range(26):
		if card["type"] & 1<<i:
			types.append(system_strings[1050+i])
	final["types"]=", ".join(types) or "None"
	attributes=[]
	for i in range(7):
		if card["attribute"] & 1<<i:
			attributes.append(system_strings[1010+i])
	final["attributes"]=", ".join(attributes) or "None"
	races=[]
	for i in range(25):
		if card["race"] & 1<<i:
			races.append(system_strings[1020+i])
	final["races"]=", ".join(races) or "None"
	final["all"]=", ".join(types+attributes+races) or "None"
	final_string=card["name"]
	if card_level>0:
		final_string+=" (level "+str(card_level)+")"
	final_string+=": ("+final["all"]+")\n"
	if card["atk"]>0 or card["def"]>0:
		final_string+=str(card["atk"])+" attack, "+str(card["def"])+" defense\n"
	final_string+=card["description"]
	final["display_string"]=final_string
	return final

cards={}
print("Attempting to download the latest yugio strings and card database...")
try:
	urlretrieve("https://raw.githubusercontent.com/shadowfox87/ygopro2/master/cdb/"+language+"/cards.cdb", "cards.cdb")
	print("downloaded "+str(os.stat("cards.cdb").st_size)+" bytes to cards.cdb...")
	urlretrieve("https://raw.githubusercontent.com/shadowfox87/ygopro2/master/config/"+language+"/strings.conf", "strings.conf")
	print("downloaded "+str(os.stat("strings.conf").st_size)+" bytes to strings.conf...")
except:
	print("There was an error with the download. now exiting")
	sys.exit()
print("successfully updated the cards database and yugio strings to the latest version!")

print("retrieving card information from database...")
db=sqlite3.connect("cards.cdb")
rawcards=db.execute("select * from 'texts';").fetchall()
for i in rawcards:
	if len(i)<18:
		continue
	card={}
	card["id"]=i[0]
	card["name"]=i[1]
	card["description"]=i[2]
	strings=[]
	for x in i[3:]:
		strings.append(x)
	card["strings"]=strings
	card_data=db.execute("select * from datas where id='"+str(card["id"])+"';").fetchone()
	if len(card_data)<10:
		continue
	card["type"]=card_data[4]
	card["atk"]=card_data[5]
	card["def"]=card_data[6]
	card["level"]=card_data[7]
	card["race"]=card_data[8]
	card["attribute"]=card_data[9]
	cards[card["id"]]=card
print("Successfully retrieved "+str(len(cards))+" cards!")

print("parsing system strings...")
system_strings={}
f=open("strings.conf", "rb")
s=f.read().split(b"\n")
f.close()
if len(s)<850:
	print("there was an error parsing the strings.conf file. now exiting")
	sys.exit()
for line in s:
	spl=line.split(b" ")
	for i in spl:
		if spl[0]==b"!system":
			f=b" ".join(spl[2:]).decode().replace(chr(0xa0), chr(0x20))
			system_strings[int(spl[1].decode())]=f
print("Successfully parsed "+str(len(system_strings))+" system strings!")

print("Writing database...")
os.mkdir("yugiohcards")
for i in cards:
	cardinfo=card_info(cards[i])
	dirs=cardinfo["all"].split(", ")
	filepath="yugiohcards/"
	if len(dirs)<0:
		continue
	elif len(dirs)<1:
		filepath+=dirs[0]
	else:
		filename=dirs[-1]
		dirs.remove(filename)
		filepath+="/".join(dirs)
		try:
			os.makedirs(filepath)
		except FileExistsError:
			pass
		filepath+="/"+filename
	filepath+=".txt"
	with open(filepath, "ab") as f:
		f.write(cardinfo["display_string"].encode()+b"\r\n\r\n")
print("Success! The card database has been written successfully! Have fun!")
