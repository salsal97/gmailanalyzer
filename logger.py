import datetime

def create_log(prefix, suffix):
    time = str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M"))
    file = open((prefix + time + suffix),"w+")
    return file
