import tkinter as tk
import tkinter.messagebox as messagebox
import win_unicode_console
from date_folder import *
from discogs_parser import *

def close_window(): 
    window.destroy()

#parsing event
def parse_items():
    item_num=item.get()
    if item_num=='': item_num='0'
    item_num=int(item_num)
    csvfile=CSV.get() #csv file for saving items
    picturesfolder=pictures_folder.get() #folder for pictures
    picturesurl=pictures_url.get()+date_folder() #url where is stored pictures at your woocommerce shop
    discogskey=key.get()

    if parse_from_discogs(discogskey,csvfile,picturesfolder,picturesurl,item_num):
       messagebox.showinfo(title='Done!', message='Import succesfully finished!')
    else: 
       messagebox.showerror(title='Warning!', message='Something went wrong!')

#GUI
win_unicode_console.enable()
window=tk.Tk()
window.title('Discogs->WooCommerce Importer')
window.geometry("410x190")

frame1 = tk.Frame(master=window, height=30)
frame1.pack(fill=tk.X)
key_label=tk.Label(master=frame1,text='Discogs Key')
key_label.pack(padx=5, pady=5,side=tk.LEFT)
key=tk.Entry(master=frame1,width=50)
key.insert(0,'ENTER YOUR DISCOGS TOKEN THERE')
key.pack(padx=5, pady=5,side=tk.RIGHT)

frame2 = tk.Frame(master=window, height=30)
frame2.pack(fill=tk.X)
CSV_label=tk.Label(master=frame2,text='CSV File')
CSV_label.pack(padx=5, pady=5,side=tk.LEFT)
CSV=tk.Entry(master=frame2,width=50)
CSV.insert(0,'discogs.csv')
CSV.pack(padx=5, pady=5,side=tk.RIGHT)

frame3 = tk.Frame(master=window, height=30)
frame3.pack(fill=tk.X)
pictures_folder_label=tk.Label(master=frame3,text='Pictures Folder')
pictures_folder_label.pack(padx=5, pady=5,side=tk.LEFT)
pictures_folder=tk.Entry(master=frame3,width=50)
pictures_folder.insert(0,'photos/')
pictures_folder.pack(padx=5, pady=5,side=tk.RIGHT)

frame4 = tk.Frame(master=window, height=30)
frame4.pack(fill=tk.X)
pictures_url_label=tk.Label(master=frame4,text='Pictures URL')
pictures_url_label.pack(padx=5, pady=5,side=tk.LEFT)
pictures_url=tk.Entry(master=frame4,width=50)
pictures_url.insert(0,'https://www.YOURSHOP.com/wp-content/uploads/')
pictures_url.pack(padx=5, pady=5,side=tk.RIGHT)

frame5 = tk.Frame(master=window, height=30)
frame5.pack(fill=tk.X)
item_label=tk.Label(master=frame5,text='Item Number')
item_label.pack(padx=5, pady=5,side=tk.LEFT)
item=tk.Entry(master=frame5,width=50)
item.pack(padx=5, pady=5,side=tk.RIGHT)

frame6 = tk.Frame(master=window, height=30)
frame6.pack(fill=tk.X)

button = tk.Button(
    master=frame6,
    text="Start!",
    width=10,
    height=1,
    fg="red",
    command = parse_items
)
button.pack(padx=60,side=tk.LEFT)

button2 = tk.Button(
    master=frame6,
    text="Quit",
    width=10,
    height=1,
    fg="red",
    command = close_window
)
button2.pack(padx=60,side=tk.LEFT)

window.mainloop()