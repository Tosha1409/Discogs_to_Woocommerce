import sys, re, discogs_client, csv

#connection to discpgs API
class Discogs_connection():
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

class Csv_file():
	def __init__(self, name):
		#forming first line with name of rows
		self.csvfile=name #csv file for saving items
		self.header=False #does file have header
	def __str__(self):
		return (self.csvfile)
	#creating file
	def add_item(self,item):
	        self.item=item
	def open_file(self): 
		self.writer = csv.writer(open(self.csvfile, 'w',encoding='utf-8'), delimiter =',', quotechar='"', lineterminator='\r')
	def write_first_row(self): #writing first row with collumn names
		self.writer.writerow(self.item.rows)	
	def write_row(self):
		#check for header
		if not self.header:
			self.write_first_row()
			self.header=True
		self.writer.writerow(self.item.line)

#picture and method to retrieve it
class Picture():
	def __init__(self,folder,info):
		self.folder=folder
		self.item_info=info
		self.picture=''
	#retriving picture
	def get_picture(self,connection):
		try:
			image = self.item_info.release.images[0]['uri']
			#parsing and downloading first image
			content, resp = connection._fetcher.fetch(None, 'GET', image, headers={'User-agent': connection.user_agent})
			self.picture=(image.split('/')[-1]).split('.')[0]+'.jpg' 
			with open(self.folder+self.picture, 'wb') as fh: fh.write(content)
			fh.close()
		except: pass

#categories
class Categories():
	def __init__(self):
		self.categories = [{'Title':'CD', 'Category':'CDs', 'Details': ['CD', '85', 'DCD', '150', 'Tripple CD', '220']}, {'Title':'Cassette', 'Category':'Tapes', 'Details': ['Tape', '65']}, \
		{'Title':'CDr', 'Category':'CDs', 'Details': ['CDR', '85']}]
		self.vinyl_categories = [{'Title': 'LP|12"', 'Category': 'Vinyls, Vinyls > LP/DLPS', 'Details': ['LP', '230', 'DLP', '460', 'Tripple LP', '690']}, \
                {'Title': '10"', 'Category': 'Vinyls, Vinyls > 10"s', 'Details': ['10"', '135', '2x10"', '270', '3x10"', '400']}, \
		{'Title': '7"', 'Category': 'Vinyls, Vinyls > 7"s', 'Details': ['7"', '60', '2x7"', '120', '3x7"', '180'] }]
		self.category = ''
		self.weight = 0
		self.format = ''
	#for inner_use
	def _parse(self,format_info,item):
		self.category=format_info.get('Category')
		details=format_info.get('Details')
		self.format=details[(int(item.release.formats[0]['qty'])-1)*2]
		self.weight=details[(int(item.release.formats[0]['qty'])-1)*2+1]
	#for inner_use (parsing format info)
	def _format_fix(self,item,format):
		#parsing additional information about release from descriptions, if it is possible, cause there is not always this information
		try:
			extra = ' '+','.join(item.release.formats[0]['descriptions'])
			prefix_words='Digipak|Digipack|Slipcase|A5 Digibook|Digibook|Digisleeve|Gatefold|Split|Jewel case|Jewelcase'
			#detecting MiniAlbums and Picture vinyls (might need to be rewritten in future)
			if (re.search('Mini-Album|EP|Mini', extra)) and ((self.format=='CD') or (self.format=='LP')): self.format = 'M'+self.format #adding M infront for minialbum releases
			if (re.search('Picture Disc', extra)): self.format = 'Picture '+self.format #adding Picture word infront of format info
			#finding additional details about format and adding it to right place, and keeping all what is left in brackets (usually it is vinyl colour and similar details) 
			extra=re.search(prefix_words, item.release.formats[0]['text']) #if any of those words found them going infront
			self.format += ' ('+re.sub(prefix_words,'',item.release.formats[0]['text']) +')'#rest goes beind in brackets
			self.format = extra.group() + ' ' + self.format
			self.format = re.sub('\(\s*\)','',self.format) #removing empty additinonal info like () or ( )
			self.format = re.sub('\(\s*((\s*\S+)*)\s*\)',  r'(\1)',self.format) #removing extra white spaces
		except: pass
	#finding category,format and weight
	def detect(self,item):
		for format_info in self.categories:
			if item.release.formats[0]['name']==format_info.get('Title'):
				self._parse(format_info,item)
				break
		if item.release.formats[0]['name']=='Vinyl':
			for format_info in self.vinyl_categories:
				if re.search(format_info.get('Title'), ','.join(item.release.formats[0]['descriptions'])): 
					self._parse(format_info,item)
					break
		self._format_fix(item,self.format)

class Item():
	def __init__(self, url, connection, folder):
		#forming first line with name of rows
		self.rows = ('ID', 'Type', 'SKU', 'Name', 'Published', 'Is featured?', 'Visibility in catalog', 'Short description', 'Description', 'Date sale price starts', \
		'Date sale price ends', 'Tax status', 'Tax class', 'In stock?', 'Stock', 'Low stock amount', 'Backorders allowed?', 'Sold individually?', 'Weight (g)', \
		'Length (cm)', 'Width (cm)', 'Height (cm)', 'Allow customer reviews?', 'Purchase note', 'Sale price', 'Regular price', 'Categories', 'Tags', 'Shipping class', \
		'Images', 'Download limit', 'Download expiry days', 'Parent', 'Grouped products', 'Upsells', 'Cross-sells', 'External URL', 'Button text', 'Position')
		self.picturesurl=url #url where is stored pictures at your woocommerce shop
		self.discogs_connection=connection
		self.picturesfolder=folder
		#self.picture=picture
	def __str__(self):
		return (self.line[3])
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
		self.line[7]=self.line[8]='<strong>('+self._artist_label_fix(label)+')</strong>'
	def set_title(self, format):
		self.line[3]=self._artist_label_fix(self._artist_fix())+' - '+str(self.item.release.title)+' '+str(format)
	def set_price(self,price):
		self.line[25]= self._price_fix(price)
	#private methods
	#parsing artist(s)
	def _artist_fix (self):
		artist = ''
		#have to be parsed this way cause it is object 
		for artists in self.item.release.artists: 
			if artist=='': artist = artists.name #if it is firt artist
			else: artist = artist +'/'+ artists.name #if there is few artists theirs names will be separated with /
		return (artist)		 				
	#parsing label(s)
	def _label_fix (self):
		label=''
		for rawdata in self.item.release.labels: label=label+str(rawdata.name)+'/'
		label=label[:-1] #removing last symbol cause it is always extra /
		return (label)
	def _artist_label_fix(self,line):
		return re.sub('\s\(\d+\)','',str(line)) 
	#fixing price since discogs using '.' and woocommerce ','.
	def _price_fix(self,line):
		return str(line).replace('.',',')
	#main parse that parse everything using previous methods
	def parser(self):
		tmp = Categories()
		tmp.detect(self.item)
		self.set_title(tmp.format)
		self.set_description(self._label_fix())
		self.set_weight(tmp.weight)
		self.set_price(self.item.price.value)
		self.set_category(tmp.category)
		pic=Picture(self.picturesfolder,self.item)
		pic.get_picture(self.discogs_connection.return_connection())
		self.set_picture(pic.picture)	 