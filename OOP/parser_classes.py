import sys, re, discogs_client, csv

#connection to discpgs API
class discogs_connection():
	#token is discogs token
	def __init__(self,token):
		self.user_token = token
	def __repr___(self):
		return (self.user_token)
	#identification
	def identify(self):
		self.connection = discogs_client.Client('ExampleApplication/0.1', user_token=self.user_token) #discogs identification
		self.me=self.connection.identity()
	#returns invetory
	def get_inventory(self):
		self.identify()
		return (self.me.inventory)
	#returns connection
	def return_connection(self):
		return (self.connection)
	#downloading picture to folder, and param is current item
	def get_picture(self,folder,param):
		try:
			image = param.release.images[0]['uri']
			#parsing and downloading first image
			content, resp = self.connection._fetcher.fetch(None, 'GET', image, headers={'User-agent': self.connection.user_agent})
			picture=(image.split('/')[-1]).split('.')[0]+'.jpg' 
			with open(folder+picture, 'wb') as fh: fh.write(content)
			fh.close()
		except: picture=''
		return (picture)

class categories():
	def __init__(self):
		self.categories = [{'Title':'CD', 'Category':'CDs', 'Details': ['CD', '85', 'DCD', '150', 'Tripple CD', '220']}, {'Title':'Cassette', 'Category':'Tapes', 'Details': ['Tape', '65']}, \
		{'Title':'CDr', 'Category':'CDs', 'Details': ['CDR', '85']}]
		self.vinyl_categories = [{'Title': 'LP|12"', 'Category': 'Vinyls, Vinyls > LP/DLPS', 'Details': ['LP', '230', 'DLP', '460', 'Tripple LP', '690']}, \
                {'Title': '10"', 'Category': 'Vinyls, Vinyls > 10"s', 'Details': ['10"', '135', '2x10"', '270', '3x10"', '400']}, \
		{'Title': '7"', 'Category': 'Vinyls, Vinyls > 7"s', 'Details': ['7"', '60', '2x7"', '120', '3x7"', '180'] }]
	#for inner use
	def parse(self,format_info,items):
		category=format_info.get('Category')
		details=format_info.get('Details')
		format=details[(int(items.release.formats[0]['qty'])-1)*2]
		weight=details[(int(items.release.formats[0]['qty'])-1)*2+1]
		return (category,format,weight)
	#finding category,format and weight
	def detect(self,items):
		category=format=weight=''
		for format_info in self.categories:
			if items.release.formats[0]['name']==format_info.get('Title'):
				category,format,weight = self.parse(format_info,items)
				break
		if items.release.formats[0]['name']=='Vinyl':
			for format_info in self.vinyl_categories:
				if re.search(format_info.get('Title'), ','.join(items.release.formats[0]['descriptions'])): 
					category,format,weight = self.parse(format_info,items)
					break
		return (category,format,weight)

class csv_file():
        ###fuctions for strings###
	#removing unnesesary (number), those happens if there is few artists or labels have same name so to separate them from each other used (2) (3) etc
	def artist_label_fix(self,line):
		return re.sub('\s\(\d+\)','',str(line)) 
	#fixing price since discogs using '.' and woocommerce ','.
	def price_fix(self,line):
		return str(line).replace('.',',')
	def __init__(self, name, url, connection,folder):
		#forming first line with name of rows
		self.rows = ('ID', 'Type', 'SKU', 'Name', 'Published', 'Is featured?', 'Visibility in catalog', 'Short description', 'Description', 'Date sale price starts', \
		'Date sale price ends', 'Tax status', 'Tax class', 'In stock?', 'Stock', 'Low stock amount', 'Backorders allowed?', 'Sold individually?', 'Weight (g)', \
		'Length (cm)', 'Width (cm)', 'Height (cm)', 'Allow customer reviews?', 'Purchase note', 'Sale price', 'Regular price', 'Categories', 'Tags', 'Shipping class', \
		'Images', 'Download limit', 'Download expiry days', 'Parent', 'Grouped products', 'Upsells', 'Cross-sells', 'External URL', 'Button text', 'Position')
		self.csvfile=name #csv file for saving items
		self.picturesurl=url #url where is stored pictures at your woocommerce shop
		self.discogs_connection=connection
		self.picturesfolder=folder
	def __str__(self):
		return (self.line[3])
	#creating file
	def open_file(self): 
		self.writer = csv.writer(open(self.csvfile, 'w',encoding='utf-8'), delimiter =',', quotechar='"', lineterminator='\r')
	#generation of new line
	def new_line(self,item): 
		self.item=item
		self.line=['']*39
		self.line[1],self.line[6],self.line[11]='simple','visible','taxable'
		self.line[4]=self.line[13]='1'
		self.line[5]=self.line[16]=self.line[17]=self.line[22]=self.line[38]='0'
	#functions for settings values
	def set_weight(self,weight):
		self.line[18]= weight
	def set_category(self,category):
		self.line[26]= category
	def set_picture(self, picture):
		self.line[29]= self.picturesurl+picture
	def set_description(self, label):
		self.line[7]=self.line[8]='<strong>('+self.artist_label_fix(label)+')</strong>'
	def set_title(self, format):
		self.line[3]=self.artist_label_fix(self.artist_fix())+' - '+str(self.item.release.title)+' '+str(self.format_fix(format))
	def set_price(self,price):
		self.line[25]= self.price_fix(price)
	def write_first_row(self): #writing first row with collumn names
		self.writer.writerow(self.rows)	
	def write_row(self):
	        self.writer.writerow(self.line)
	#parsing artist(s)
	def artist_fix (self):
		artist = ''
		#have to be parsed this way cause it is object 
		for artists in self.item.release.artists: 
			if artist=='': artist = artists.name #if it is firt artist
			else: artist = artist +'/'+ artists.name #if there is few artists theirs names will be separated with /
		return (artist)		 				
	#parsing label(s)
	def label_fix (self):
		label=''
		for rawdata in self.item.release.labels: label=label+str(rawdata.name)+'/'
		label=label[:-1] #removing last symbol cause it is always extra /
		return (label)
	#parsing format info
	def format_fix(self,format):
		#parsing additional information about release from descriptions, if it is possible, cause there is not always this information
		try:
			extra = ' '+','.join(self.item.release.formats[0]['descriptions'])
			prefix_words='Digipak|Digipack|Slipcase|A5 Digibook|Digibook|Digisleeve|Gatefold|Split|Jewel case|Jewelcase'
			#detecting MiniAlbums and Picture vinyls (might need to be rewritten in future)
			if (re.search('Mini-Album|EP|Mini', extra)) and ((format=='CD') or (format=='LP')): format = 'M'+format #adding M infront for minialbum releases
			if (re.search('Picture Disc', extra)): format = 'Picture '+format #adding Picture word infront of format info
			#finding additional details about format and adding it to right place, and keeping all what is left in brackets (usually it is vinyl colour and similar details) 
			extra=re.search(prefix_words, self.item.release.formats[0]['text']) #if any of those words found them going infront
			format += ' ('+re.sub(prefix_words,'',self.item.release.formats[0]['text']) +')'#rest goes beind in brackets
			format = extra.group() + ' ' + format
			format = re.sub('\(\s*\)','',format) #removing empty additinonal info like () or ( )
			format = re.sub('\(\s*((\s*\S+)*)\s*\)',  r'(\1)',format) #removing extra white spaces
		except: pass
		return (format)
	#main parse that parse everything using previous methods
	def parser(self):
		tmp = categories()
		category,format,weight = tmp.detect(self.item)
		self.set_title(format)
		self.set_description(self.label_fix())
		self.set_weight(weight)
		self.set_price(self.item.price.value)
		self.set_category(category)
		self.set_picture(self.discogs_connection.get_picture(self.picturesfolder,self.item))