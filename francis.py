'''
francis.py

A script for walking through directories of mostly images, recoding as much 
information about them as possible, and creating a tab-delimited output file.

Prerequisites
python3


'''
import os, datetime, time, re
from os.path import join, getsize

# SETUP

outputfilename = "digitalarchive_170615" # set this to what your outputfile name - maybe autocreate?
directorytoscanfrom = "U:\Bulk\LibraryDigital\DigitalArchive" # top directory to start scanning from

def ucode(text):
    # replace odd characters in filenames - quotes, and other weirdness
    text = text.replace("\u2019","'")
    text = text.replace('\u201c','"')
    text = text.replace('\u201d','"')
    text = text.replace('\uf020','?')
    text = text.replace('\uf022','?')
    return text

def sizeof_fmt(num, suffix='B'):
    # format from bytes to nice human readable units
    for unit in ['',' K',' M',' G',' T',' P',' E',' Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def findfiletype(text):
    # try and find file extensions starting with a full stop, then 1 to 5 chars long, or return 'error'
    regex = r'\.([a-zA-Z1-9]{1,5}\b$)'
    try:
        match = re.findall(regex, text, re.MULTILINE)[-1] 
        #the last item in an array of matches, so at the end of the line
    except:
        match = "error"
        print(text) #output the text causing the error to standard output
    return match
   
# variable initialisations
dirsize = 0 # this will increment as each file is recorded
filedetails = '' #this will hold lines of file information, and then we write the file information after the directory.


outputfile = open(outputfilename, 'w') 

# write a header row 
outputfile.write(
    "location \t \
    file/directory \t \
    filename \t \
    filtetype \t \
    # sub directories \t \
    #  files in subdirectories \t \
    # size (nice) \t \
    # size (bytes) \t \
    # date created \t \
    # date modified \n"
    )

for root, dirs, files in os.walk(directorytoscanfrom):
    
    for name in files:
        path = os.path.join(root, name)
        try: # not all files seem amenable  to getting date and filesize
            filesize = os.path.getsize(path)
            created = datetime.datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y-%m-%d")
            modified = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d")
        except:
            filesize = 0
            created = '99-99-99'
            modified = '99-99-99'
        dirsize = dirsize + filesize
        filetype =  findfiletype(name)
        filedetails =  filedetails + ucode(root) + "\t" + "file" + "\t" +ucode(name) +  "\t" + filetype + "\t\t\t" + sizeof_fmt(filesize) + "\t" + str(filesize) + "\t"+  created + "\t" +  modified + "\n"
    dircreated = datetime.datetime.fromtimestamp(os.path.getctime(root)).strftime("%Y-%m-%d")
    dirmodified = datetime.datetime.fromtimestamp(os.path.getmtime(root)).strftime("%Y-%m-%d")
    outputfile.write(
        ucode(root)+ "\t" + \
        'directory'+ "\t\t\t" +  \
        str(len(dirs))+ "\t" +  \
        str(len(files))+ "\t" +  \
        sizeof_fmt(dirsize)+ "\t" + \
        str(dirsize) + "\t" +  \
        dircreated+ "\t" +  \
        dirmodified + "\n"\
        )
    outputfile.write(filedetails)
    dirsize = 0
    filedetails = ''

outputfile.close()