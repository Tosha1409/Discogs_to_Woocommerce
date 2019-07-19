import sys, re, discogs_client, csv, win_unicode_console
from parser_classes import *
from discogs_client.exceptions import HTTPError
win_unicode_console.enable()

#settings and identification
csvfile='discogs.csv' #csv file for saving items
picturesfolder='photos/' #folder for pictures
picturesurl='http://www.woodcutrecords.fi/wp-content/uploads/2019/06/' #url where is stored pictures at your woocommerce shop

connection = discogs_connection("ENTER YOUR TOKEN THERE")
results=connection.get_inventory()
writer = csv_file(csvfile,picturesurl,connection,picturesfolder)
writer.open_file()
writer.write_first_row()
for items in results:
	#taking items that are for sale only (cause rest is private collection etc)
	if items.status == "For Sale":
		writer.new_line(items)
		writer.parser()
		writer.write_row()
		print (u'Parsing - '+str(writer))
print ('Finished!')