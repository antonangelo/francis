import os, datetime, time, re, magic, wand, exifread
from os.path import join, getsize
from wand.image import Image

def ucode(text):
    text = text.replace("\u2019","'")
    text = text.replace('\u201c','"')
    text = text.replace('\u201d','"')
    text = text.replace('\uf020','?')
    text = text.replace('\uf022','?')
    return text

def sizeof_fmt(num, suffix='B'):
    for unit in ['',' K',' M',' G',' T',' P',' E',' Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def findfiletype(text):
    regex = r'\.([a-zA-Z1-9]{1,5}\b$)'
    try:
        match = re.findall(regex, text, re.MULTILINE)[-1]
    except:
        match = "error"
        print(text)
    return match
   
dirsize = 0
filedetails = ''
outputfile = open('output_170613.tsv', 'w')

outputfile.write(
    "location \t file/directory \t filename \t filtetype \t # sub directories \
    \t # files in subdirectories \t size (nice) \t size (bytes) \
    \t date created \t date modified \t fileinfo \t imagewidth \t \
    imageheight \t imagedepth \t imageresolution \t imagetype \t exifdata \n")

for root, dirs, files in os.walk('data'):
    
    for name in files:
        path = os.path.join(root, name)
        try: 
            filesize = os.path.getsize(path)
            created = datetime.datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y-%m-%d")
            modified = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d")
        except:
            filesize = 0
            created = '99-99-99'
            modified = '99-99-99'
        with magic.Magic() as m:
            fileinfo = m.id_filename(path)
            #print(fileinfo)
        try:
            with Image(filename=path) as i:
                imagewidth = i.width
                imageheight = i.height
                imagedepth = i.depth
                imageresolution = i.resolution
                imagetype = i.type
                print( imagewidth, imageheight, imagedepth, imageresolution, imagetype)
        except:
            imagesize = 0
        # print(imagesize)
        imageforexiftags = open(path, 'rb')
        tags = exifread.process_file(imageforexiftags, details='False')
        exifdata = ""
        for tag in tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                exifdata = exifdata + str(tag) + ": "+ str(tags[tag]) + " , " 
        # print(exifdata)
        dirsize = dirsize + filesize
        filetype =  findfiletype(name)
        filedetails =  filedetails + ucode(root) + "\t" + "file" + "\t" +ucode(name) + "\t" + \
        filetype + "\t\t\t" + sizeof_fmt(filesize) + "\t" + str(filesize) + "\t"+  created + "\t" +\
        modified +  "\t" + fileinfo + "\t" + exifdata + str(imagewidth) +  "\t" + str(imageheight) +  "\t" +\
        str(imagedepth) +  "\t" + str(imageresolution) +  "\t" + imagetype + "\n"

    dircreated = datetime.datetime.fromtimestamp(os.path.getctime(root)).strftime("%Y-%m-%d")
    dirmodified = datetime.datetime.fromtimestamp(os.path.getmtime(root)).strftime("%Y-%m-%d")
    outputfile.write(
        ucode(root) + "\t" + "directory" + "\t\t\t" +  str(len(dirs))+ "\t" +  \
        str(len(files))+ "\t" +  sizeof_fmt(dirsize)+ "\t" + str(dirsize) + "\t" +  \
        dircreated + "\t" +  dirmodified + "\n")
    outputfile.write(filedetails)
    dirsize = 0
    filedetails = ''

outputfile.close()