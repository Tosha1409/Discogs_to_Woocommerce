# Discogs_to_Woocommerce
Parser that collect photos and info from **Discogs** and putting it to CSV file that can be imported to **WooCommerce**. It doesnt handle 
(at least yet) 100% of info that included at discogs. But parse correctly over 99% of items and all pictures and that can save many
hours of work. Beside that it is hard to make 100% universal versions for all needs, because discogs info structure and different needs 
for every case.  
at OOP folder you can find object version of script(not perfect either).  
  
**and here is how to use script:**  
1. If you run it not under windows then remove line 3, and win_unicode_console from first line.  
2. Get discogs tokken for your acccount (more info/place to request https://www.discogs.com/developers/ ).  
3. Edit variables/setting at script that you want to change.  
4. Run and get your *CSV* file.
  
and **OOP** folder includes:  
**parser_classes.py** - classes.  
**api.py** - parser that parsing all items for sale.  
**api_with_listing_number.py** -  parser that parsing only items that have *particular(or higher)* item ID. It works pretty slowly because it is goes through all items, but it is still many times faster then make it manually. Unfortuantely, discogs is great webpage, but **Discogs API** is not that good as page itself, and documentation is even worse (if you check any resourse online that you can see it easily). And it makes development too complicated.
  
let me know if you have any questions.
