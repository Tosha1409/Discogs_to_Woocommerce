import sys, re, discogs_client, csv, win_unicode_console
from tqdm import tqdm
from parser_classes import *
from date_folder import *
from discogs_client.exceptions import HTTPError
win_unicode_console.enable()

#settings and identification
csvfile='discogs.csv' #csv file for saving items
picturesfolder='photos/' #folder for pictures
picturesurl='YOUR URL'+date_folder() #url where is stored pictures at your woocommerce shop

try:
	connection = Discogs_connection("ENTER YOUR TOKEN THERE")
	results=connection.get_inventory()
	i = Item(picturesurl,connection,picturesfolder)
	writer = Csv_file(csvfile)
	writer.open_file()
	writer.add_item(i)
	print ('Amount of items -', len(results))
	for item in tqdm(results):
		#taking items that are for sale only (cause rest is private collection etc)
		if (item.status == "For Sale") and (item.id>=int(sys.argv[1])):
			i.new_line(item)
			i.parser()
			writer.write_row()
except: pass
print ('Finished!')