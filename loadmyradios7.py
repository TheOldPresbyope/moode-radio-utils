#!/usr/bin/python3

# 20201219 THIS IS A SPECIAL EDITION CREATED SOLELY TO LOAD DATA INTO moOde 7.0.0 
# FROM the myradios.tar.gz FILE CREATED IN moOde 6.7.1 BY THE EXISTING 
# V2.0 utility savemyradios.py

# moOde utility to load user-defined radio stations into moOde
# from myradios.tar.gz in the current working directory
# the myradios.tar.gz file is created by the companion utility savemyradios.py
#
# Rev 2/20200822 - revamp for moOde r660 changes to database schema
#                  and locations of radio-related files; not compatible
#                  with previous releases of moOde or savemyradio.py
#                  or their myradios.tar.gz files
#
# script must be invoked as superuser because of moOde's directory permissions
# e.g., sudo ./loadmyradios.py
#
# existing user-defined radio stations are not touched and matching entries
# from myradios.tar.gz are skipped.

# author: TheOldPresbyope, 20190813

# TODO - perhaps never;)
#  - allow user to input an alternative tar file name (less the .tar.gz suffix)
#  - allow user to select which stations to load
#  - make more Pythonic so I'm not embarrassed to show it

import glob, json, os, shutil, sqlite3, subprocess, sys, tarfile, tempfile 

try:
  from PIL import Image
except:
  print("Oops, need to install Python Imaging Library package first")
  print("first, run 'sudo apt install python3-pil'")
  sys.exit("then invoke again")

print("Load user-defined radio stations into moOde 7.0.0 from myradios.tar.gz file in the current working directory")

if os.geteuid() != 0:
  print("Oops, we need superuser privileges. Invoke again using sudo")
  sys.exit()

# cute trick found in maroc81 comment to https://gist.github.com/garrettdreyfus/8153571
if not input("Proceed? (y/n): ").lower().strip()[:1] == "y": sys.exit(1)

myfile = 'myradios.tar.gz'

# moode-specific locations

# be mindful of '/'
moodesqlite3='/var/local/www/db/moode-sqlite3.db'
RADIOdest = '/var/lib/mpd/music/RADIO/'
logodest = '/var/local/www/imagesw/radio-logos/'
thumbdest = logodest+'thumbs/'

if not os.path.isfile(myfile):
  print("Oops, couldn't find {}".format(myfile))
  sys.exit()

try:
  conn = sqlite3.connect(moodesqlite3)
except:
  print("Oops, couldn't connect to {}".format(moodesqlite3))
  sys.exit()

# create a temporary work space: note that by defining the obj first, Python
# will automatically remove the tmpdir on exit
tmpdirobj=tempfile.TemporaryDirectory()
tmpdir=tmpdirobj.name

#  be mindful of  '/' 
RADIOsrc = tmpdir+'/RADIO/'
logosrc = tmpdir+'/logos/'
thumbsrc = logosrc+'thumbs/'

tar = tarfile.open(myfile)
tar.extractall(path=tmpdir)
tar.close()

# moOde 6.7.1
# cfg_radio schema: (id , station , name , type , logo,
#                    genre, broadcaster, language, country,
#                    region, bitrate, format)
#
# moOde 7.0.0
# cfg_radio schema: (id , station , name , type , logo,
#                    genre, broadcaster, language, country,
#                    region, bitrate, format, 
#                    geo-fenced, reserved1, reserved2)
#
# where:
#    'id' is an integer primary key
#    'station' is the station URL
#    'name' is the station name (which is used as the root of the .pls
#      and .jpg files, but see also logo)
#    'type' (6.7.1) is 'u' for user-defined or 's' for system-defined 
#    'type' (7.0.0) is 'r' for regular, 'f' for favorite, or 'h' for hidden 
#    'logo' (6.7.1) is a filepath or 'local'; user-defined stations appear
#           always to have logo='local' 
#    'logo' (7/.0.0) appears always to be 'local'
#    'geo-fenced' is 'No' or 'Yes'
#    and the remaining columns are informative text descriptors 
#    which are self-evident except possibly:
#    'format' is intended to represent audio encoding such as 'MP3' 

myfile = open(tmpdir+'/radios.json','r')
radios=json.load(myfile)
myfile.close()

# for each entry get name, check that it's not already in cfg_radio
# if not insert the new entry (with NULL -- 'None' in Python -- for id to bump
# bump it from previous value) and copy .pls file and .jpg files to destinations

rowsadded=0

for entry in radios:
  name = entry['name']
  cur = conn.cursor()
  cur.execute("SELECT * FROM cfg_radio WHERE name=?", (name,))
  if cur.fetchone():
    print("skipping duplicate entry: name= '{}'".format(name))
    continue

  # get here if entry not already in table (jury seems to be out on reusing cursor or not so I don't) 
  print("adding station '{}'".format(name))
  cur = conn.cursor()
  # special edition: overwrite or create column values as needed for moOde 7.0.0
  entry['logo'] = 'local'
  entry['type'] = 'r'
  entry['geo-fenced'] = 'No'
  entry['reserved1'] = ''
  entry['reserved2'] = ''

  # following command assumes order of columns. The more complicated named-based
  # access to columns might be more future-proof
  cur.execute("INSERT INTO cfg_radio VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (None,
               entry['station'],
               name,
               entry['type'],
               entry['logo'],
               entry['genre'],
               entry['broadcaster'],
               entry['language'],
               entry['country'],
               entry['region'],
               entry['bitrate'],
               entry['format'],
               entry['geo-fenced'],
               entry['reserved1'],
               entry['reserved2']
               ))
  conn.commit()
  RADIOfile=RADIOsrc+name+'.pls'
  shutil.copy(RADIOfile,RADIOdest)

  # now deal with logo image files
  # note that no image file may have been created by user
  # but if one was, make sure we have thumbnail and thumbnail_sm versions too
  logofile=logosrc+name+'.jpg'
  if os.path.isfile(logofile):
    shutil.copy(logofile,logodest)
    thumbfile=thumbsrc+name+'.jpg'
    if os.path.isfile(thumbfile):
      shutil.copy(thumbfile,thumbdest) 
    else:
      newthumb=Image.open(logofile)
      newthumb.thumbnail((200,200))
      newthumb.save(thumbdest)
    thumb_sm=Image.open(logofile)
    thumb_sm.thumbnail((80,80))
    thumb_sm.save(thumbdest+name+'_sm.jpg')
  rowsadded+=1

print("{} station(s) loaded".format(rowsadded))

# finally, force mpd to pickup the changes by bumping the times on all the 
# .pls files in the RADIO directory and dropping into the shell to run mpc.

for fn in glob.iglob(RADIOdest+'/*.pls'):
  os.utime(fn)

subprocess.run(['/usr/bin/mpc','update','RADIO'],stdout=subprocess.DEVNULL)
# the above is pretty raw--no error checking, throw stdout into the bit bucket

# note that Python cleans up the tmpdir automagically when we leave
print("The Library Radio view may need to be refreshed to display the loaded stations.")
