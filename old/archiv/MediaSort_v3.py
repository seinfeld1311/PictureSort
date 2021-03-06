# -*- coding: utf-8 -*-
__author__ = "Eric Fries"
__copyright__ = "Copyright 2018, Eric Fries"
__license__ = "GPL"
__version__ = "3.0"
__maintainer__ = "Eric Fries"
__email__ = "ich@ericfries.de"
__status__ = "Production"
__last_edited__ = "2018-14-05"

"""
The Script can be used to sort media Files (jpg/raw/mp4...) in a base folder
named after the file extension (picture/movie extension " jpg " )
with sub folders named after the exif Date/Created date of the corresponding media files.
For example: 
jpeg (base folder)
    - 2018-03-18 (sub folder)
mp4 (base fold)
    - 2018-03-18 (sub folder)
    

To use the script for other media files you must expand one of the dicts in the config_dict.py with the file extensions 
you need.


    
    BEWARE:
    https://pypi.python.org/pypi/ExifRead
    Exifread had to be changed in order to read the Lumix GX80 RW2 files 
    -> https://github.com/pypa/pypi-legacy/issues/734

TODO: log File and self created pictures without Exif creates Error "ExifError" -> must be fixed


"""

import config_dict
import exifread
import os
import shutil
import sys
import time


# The *.lower() method, is used to ignore any casessnsitivity issues with the file extension. Another benefit is that
# the Dict (endungen) can be much shorter.
def sort(endungen_exif, endungen_created, in_folder):
    os.chdir(in_folder)
    direc = os.getcwd()
    delliste = []
    with open("log.txt", "w") as logfile:
        for i in filter(os.path.isfile, os.listdir(direc)):  # Searches for media files in folder
            try:
                imagepath = os.path.join("./", i)  # create the path to the picture/media file
                endung = i.split(".")[1]  # get rid of the file extension
                if endung.lower() in endungen_exif:  # The if in part is looking for correspodent file extensions in
                    # folder and dictionary.
                    shtime = readexifdate(imagepath)  # reading the EXIF date
                    pfad = os.path.join("./", endungen_exif[endung.lower()], shtime)
                    if not os.path.exists(pfad):
                        os.makedirs(pfad)
                    shutil.move(imagepath, pfad)
                elif endung.lower() in endungen_created:
                    shtime = mp4_date(i)  # mp4 Created Date
                    pfad = os.path.join("./", endungen_created[endung.lower()], shtime)
                    if not os.path.exists(pfad):
                        os.makedirs(pfad)
                    shutil.move(imagepath, pfad)
                else:
                    pass
                    print "passed"
            except shutil.Error:
                logfile.writelines("Datei {} existiert bereits\n".format(i))
                delliste.append(i)
                print "Datei {} existiert bereits".format(i)
                pass
            except RuntimeError:
                print sys.exc_info()
                logfile.writelines("\nRuntime Error: {0} - "
                                   "{1} bei Datei: {2}\n".format(sys.exc_info()[0], sys.exc_info()[1], i))
                print "Fehler: {} - {} \nbei Datei: {}".format(sys.exc_info()[0], sys.exc_info()[1], i)
    del_log("log.txt")
    # This part let the user decide if the unnecessary / second copies of the files can be erased or not
    if len(delliste) > 0:
        delfiles = raw_input("Sollen die doppelten Dateien geloescht werden (J/N) ?: ")
        if delfiles.lower() == "j":
            del_existingfiles(delliste)
    else:
        pass


def readexifdate(imagepath):  # Function for getting the Exifdate from the pictures
    f = open(imagepath, 'rb')
    tags = exifread.process_file(f)
    exif_time = str(tags["EXIF DateTimeDigitized"]).split(" ")[0]
    shoot_time = exif_time.replace(":", "-")
    return shoot_time # With modification of the shooting time i.a. slicing it is possible to limit the folder depth from day to month [0:7]-> THis is mont "2018-12"

    # Function for getting the creation Date from the video files (with this funct it is possible to
    # get the creation date of a random file, not only media).


def mp4_date(mp4):
    ctd = time.localtime(os.path.getmtime(mp4))
    year = str(ctd.tm_year)
    mon = str(ctd.tm_mon)
    day = str(ctd.tm_mday)
    if len(mon) < 2:
        mon = "0" + mon
    if len(day) < 2:
        day = "0" + day
    ordnername = year + "-" + mon + "-" + day  # Formatting the creation date
    return ordnername


def del_log(logfile):  # This Function erases the logfile if it's empty
    if (os.stat(logfile).st_size == 0) is True:
        os.remove(logfile)


def del_existingfiles(delliste):
    for i in delliste:
        os.remove(i)


if __name__ == "__main__":
    # -> Media with readable exif files (raw/ Pictures) File extensions from the media files in front as key and
    # the folder to be created as value

    # -> Media without readable Exif Files / File extensions from the media files in front as key and the folder
    # to be created as value

    photo_folder = raw_input("Media folder: ")
    sort(config_dict.endungen_exif, config_dict.endungen_created, photo_folder)

    # BEWARE:
    # https://pypi.python.org/pypi/ExifRead
    # Exifread had to be changed in order to read the Lumix GX80 RW2 files
    # -> https://github.com/pypa/pypi-legacy/issues/734
 #TODO: Anzahl der geloeschten und Uebertragenen Dateien am Ende anzeigen