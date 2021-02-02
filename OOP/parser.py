import win_unicode_console
from discogs_parser import *
from date_folder import *

win_unicode_console.enable()

#settings and identification
csvfile='discogs.csv' #csv file for saving items
picturesfolder='photos/' #folder for pictures
picturesurl='https://www.YOURSHOP.com/wp-content/uploads/'+date_folder() #url where is stored pictures at your woocommerce shop
discogskey="ENTER YOUR DISCOGS TOKEN THERE" #token

#number of first item on discogs(taken from command line parameter, if it is not given then 0
if len(sys.argv)==1: num = 0
else: num = int(sys.argv[1])

if parse_from_discogs (discogskey,csvfile,picturesfolder,picturesurl,num): print ('Finished!')
else: print ('Something went wrong!')