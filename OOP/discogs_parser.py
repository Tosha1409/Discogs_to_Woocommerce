from tqdm import tqdm
from parser_classes import *
from discogs_client.exceptions import HTTPError

#parsing items from discogs and saving in CSV file
def parse_from_discogs (discogskey,csvfile,picturesfolder,picturesurl,item_num):
	status=True
	try:
		connection = Discogs_connection(discogskey)
		results=connection.get_inventory()
		i = Item(picturesurl,connection,picturesfolder)
		writer = Csv_file(csvfile)
		writer.open_file()
		writer.add_item(i)
		print ('Amount of items -', len(results))
		for item in tqdm(results):
			#taking items that are for sale only (cause rest is private collection etc)
			if (item.status == "For Sale") and (item.id>=item_num):
				i.new_line(item)
				i.parser()
				writer.write_row()
	except: status=False
	return status