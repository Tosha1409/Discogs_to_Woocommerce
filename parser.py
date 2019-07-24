import sys, re, discogs_client, csv, win_unicode_console
from discogs_client.exceptions import HTTPError
win_unicode_console.enable()

#removing unnesesary (number), those happens if there is few artists or labels have same name so to separate them from each other used (2) (3) etc
def artist_label_fix(line):
	return re.sub('\s\(\d+\)','',str(line)) 

#fixing price since discogs using '.' and woocommerce ','.
def price_fix(line):
	return str(line).replace('.',',')

#settings and identification
csvfile='discogs.csv' #csv file for saving items
picturesfolder='photos/' #folder for pictures
picturesurl='YOUR URL' #url where is stored pictures at your woocommerce shop
categorieslist=['CDs','Vinyl', 'Tapes', 'Vinyls > 7"s', 'Vinyls > 10"s', 'Vinyls > LP/DLPS'] #names of categories
weights=['85', '230', '135', '60', '65', '460', '690', '270', '400', '150' ,'220', '120', '180'] #weights of different items
d = discogs_client.Client('ExampleApplication/0.1', user_token="ENTER YOUR TOKEN THERE") #discogs identification
me = d.identity()

#requesting inventory
results = me.inventory

#making CSV file forming first line with name of rows
writer = csv.writer(open(csvfile, 'w',encoding='utf-8'), delimiter =',', quotechar='"', lineterminator='\r')
writer.writerow(('ID', 'Type', 'SKU', 'Name', 'Published', 'Is featured?', 'Visibility in catalog', 'Short description', 'Description', 'Date sale price starts', \
'Date sale price ends', 'Tax status', 'Tax class', 'In stock?', 'Stock', 'Low stock amount', 'Backorders allowed?', 'Sold individually?', 'Weight (g)', \
'Length (cm)', 'Width (cm)', 'Height (cm)', 'Allow customer reviews?', 'Purchase note', 'Sale price', 'Regular price', 'Categories', 'Tags', 'Shipping class', \
'Images', 'Download limit', 'Download expiry days', 'Parent', 'Grouped products', 'Upsells', 'Cross-sells', 'External URL', 'Button text', 'Position'))

#parsing all items "for sale"
for items in results:
	#taking items that are for sale only (cause rest is private collection etc)
	if items.status == "For Sale":
		#parsing artist 
		artist = ''
		#have to be parsed this way cause it is object 
		for artists in items.release.artists: 
			if artist=='': artist = artists.name #if it is firt artist
			else: artist = artist +'/'+ artists.name #if there is few artists theirs names will be separated with /
		#parsing release format finding out categories (CDs first) and weight of items
		if items.release.formats[0]['name']=='CD': 
			category,format,weight = categorieslist[0], 'CD', weights[0]
			if items.release.formats[0]['qty']=='2': format,weight = 'DCD',weights[9] #DCD
			elif items.release.formats[0]['qty']=='3': format,weight = 'Tripple CD',weights[10] #Tripple CD
                #vinyls next (done in similar way as CDs).
		elif items.release.formats[0]['name']=='Vinyl': 
			category,format = categorieslist[1], ''
			#LPs
			if re.search('LP|12"', ','.join(items.release.formats[0]['descriptions'])): 
				category,format,weight=category+', '+categorieslist[5], 'LP',weights[1]
				if items.release.formats[0]['qty']=='2': format,weight = 'DLP', weights[5]
				elif items.release.formats[0]['qty']=='3': format,weight = 'Tripple LP', weights[6]
			#10inches
			elif re.search('10"', ','.join(items.release.formats[0]['descriptions'])): 
				category,format,weight=category+', '+categorieslist[4], '10"', weights[2]
				if items.release.formats[0]['qty']=='2': format,weight = '2x10"', weights[7]
				elif items.release.formats[0]['qty']=='3': format,weight = '3x10"', weights[8]
			#inches
			elif re.search('7"', ','.join(items.release.formats[0]['descriptions'])): 
				category,format,weight=category+', '+categorieslist[3], '7"', weights[3]
				if items.release.formats[0]['qty']=='2': format,weight = '2x7"', weights[11]
				elif items.release.formats[0]['qty']=='3': format,weight = '3x7"', weights[12]
	        #and finally tapes
		elif items.release.formats[0]['name']=='Cassette': category,format,weight = categorieslist[2], 'Tape', weights[4]
		#parsing additional information about release from descriptions, if it is possible, cause there is not always this information
		try:
			tmp = ' '+','.join(items.release.formats[0]['descriptions'])
			#detecting MiniAlbums and Picture vinyls
			if (re.search('Mini-Album|EP|Mini', tmp)) and ((format=='CD') or (format=='LP')): format = 'M'+format #adding M infront for minialbum releases
			if (re.search('Picture Disc', tmp)): format = 'Picture '+format #adding Picture word infront of format info
			#finding additional details about format and adding it to right place, and keeping all what is left in brackets (usually it is vinyl colour and similar details) 
			tmp=re.search('Digipak|Digipack|Slipcase|A5 Digibook|Digibook|Digisleeve|Gatefold|Split|Jewel case|Jewelcase', items.release.formats[0]['text']) #if any of those words found them going infront
			format += ' ('+re.sub('Digipak|Digipack|Slipcase|A5 Digibook|Digibook|Digisleeve|Gatefold|Split|Jewel case|Jewelcase','',items.release.formats[0]['text']) +')'
			format = tmp.group() + ' ' + format
			format = re.sub('\(\s*\)','',format) #removing empty additinonal info like () or ( )
			format = re.sub('\(\s*((\s*\S+)*)\s*\)',  r'(\1)',format) #removing extra white spaces
		except: pass
		#not in use
		link = 'https://www.discogs.com/sell/item/'+str(items.id)
		#have to be parsed this way cause it is object
		label=''
		for rawdata in items.release.labels: label=label+str(rawdata.name)+'/'
		label=label[:-1] #removing last symbol cause it is always extra /
		#parsing and downloading first image
		try:
			image = items.release.images[0]['uri']
			content, resp = d._fetcher.fetch(None, 'GET', image, headers={'User-agent': d.user_agent})
			picture=(image.split('/')[-1]).split('.')[0]+'.jpg' 
			with open(picturesfolder+picture, 'wb') as fh:
				fh.write(content)
		except: image =''

		#parsing correct values to rows
		line =['']*39
		line[1]='simple'
		line[3]=artist_label_fix(artist)+' - '+str(items.release.title)+' '+str(format)
		line[4]=line[13]='1'
		line[5]=line[16]=line[17]=line[22]=line[38]='0'
		line[6]='visible'
		line[7]=line[8]='<strong>('+artist_label_fix(label)+')</strong>'
		line[11]='taxable'
		line[18]= weight
		line[25]= price_fix(items.price.value)
		line[26]= category
		line[29]= picturesurl+picture
		#writing line to file and putting item to screen
		writer.writerow(line)
		print (u'Parsing - '+(line[3]))
print ('Finished!')