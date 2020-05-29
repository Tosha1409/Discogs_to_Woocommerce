import datetime
def date_folder():
    return (str(datetime.datetime.today().year)+'/'+str('%02d' % (datetime.datetime.today().month))+'/')