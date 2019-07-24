import sys, re, discogs_client, csv, win_unicode_console
from parser_classes import *
from discogs_client.exceptions import HTTPError
win_unicode_console.enable()

#settings and identification
csvfile='discogs.csv' #csv file for saving items
picturesfolder='photos/' #folder for pictures
picturesurl='YOUR URL' #url where is stored pictures at your woocommerce shop

try:
	connection = discogs_connection("ENTER YOUR TOKEN THERE")
	results=connection.get_inventory()
	writer = csv_file(csvfile,picturesurl,connection,picturesfolder)
	writer.open_file()
	writer.write_first_row()
	for items in results:
	#taking items that are for sale only (cause rest is private collection etc)
		if (items.status == "For Sale") and (items.id>=int(sys.argv[1])):
			writer.new_line(items)
			writer.parser()
			writer.write_row()
			print (u'Parsing - '+str(writer))
except: pass
print ('Finished!')