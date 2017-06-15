# francis

This script works through a number of folders and 
saves information about them, in particular images, 
to an output file, and errors to standard out.

Named after Francis Yapp, as this script does his 
job for him.

* francis.py works only with inbuilt python3 modules
* francis+.py also reads EXIF data, uses imagemagik bindings to get image data, and 'magic' to get file information, it requires;
    * filemagic https://pypi.python.org/pypi/filemagic
    * Wand https://pypi.python.org/pypi/Wand/0.4.4 
    * ExifRead https://pypi.python.org/pypi/ExifRead/2.1.2 

<anton@angelo.nz> 
