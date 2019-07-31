import sys, re, discogs_client, csv, win_unicode_console
from parser_classes import *
from discogs_client.exceptions import HTTPError
win_unicode_console.enable()

#settings and identification
csvfile='discogs.csv' #csv file for saving items
picturesfolder='photos/' #folder for pictures
picturesurl='YOUR URL' #url where is stored pictures at your woocommerce shop

try:
	connection = Discogs_connection("ENTER YOUR TOKEN THERE")
	results=connection.get_inventory()
	i = Item(picturesurl,connection,picturesfolder)
	writer = Csv_file(csvfile)
	writer.open_file()
	writer.add_item(i)
	writer.write_first_row()
	for item in results:
		#taking items that are for sale only (cause rest is private collection etc)
		if (item.status == "For Sale") and (items.id>=int(sys.argv[1])):
			i.new_line(item)
			i.parser()
			writer.write_row()
			print (u'Parsing - '+str(i))
expect: pass
print ('Finished!')