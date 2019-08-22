#!/usr/bin/python3

# moOde utility to save user-defined radio stations
# Rev 1/20190822 - tell user and don't create empty tar file if
#                  no usable stations found
#
# Select all user-defined radio stations entries in table cfg_radio 
# in /var/local/www/db/moode-sqlite3.db and use the data to select
# the associated .pls files and .jpg files.
#
# Save everything as a tarball 'myradios.tar.gz' in current working
# directory for reuse on same or different moOde player

# The structure of the tarball contents is:
# ./radios.json  --- file containing the selected cfg_radio entries;
#                    'id' is removed because it is irrelevant in exchange
#                    while 'type' and 'logo' are retained for possible
#                    use even though at present they appear always
#                    another db while type and logo appear always
#                    to be 'u' and 'local' for user-defines
# ./RADIO        --- dir containing all the .pls files
# ./logos        --- dir containing the logo .jpg files if they exist
# ./logos/thumbs --- dir containing the thumb jpg files if they exist 

# Assumptions:
#   1) all user-defined stations appear in cfg_radio and are tagged
#      type='u' 
#   2) there is a 1-to-1 correspondence between cfg_radio entries
#      and .pls files. 
#   ***In particular, this script ignores cfg_entries with no
#      corresponding .pls file and does not account for any user-added 
#      .pls files which don't correspond to a cfg_radio entry.***

# Creates a temporary directory for working space and deletes it when done

# author: TheOldPresbyope, 20190813

# TODO -- perhaps never;)
# - allow user to input a alternative tar file name (less the .tar.gz suffix).
# - allow user to select which user-defined radio stations to save
# - make more Pythonic so I won't be embarrassed to show it 


import json, os, shutil, sqlite3, sys, tempfile

# moode-specific locations
moodesqlite3 = '/var/local/www/db/moode-sqlite3.db'
RADIOsrc = '/var/lib/mpd/music/RADIO/'
logosrc = '/var/www/images/radio-logos/'
thumbsrc = logosrc+'thumbs/'

print("Save user-defined radio stations to 'myradios.tar.gz' in the")
print("current working directory, overwriting existing file if present")

# cute trick found on Stack Overflow
if not input("Proceed? (y/n): ").lower().strip()[:1] == "y": sys.exit(1)

try:
  conn = sqlite3.connect(moodesqlite3)
except:
  print("Couldn't connect to " + moodesqlite3)
  sys.exit()

# cfg_radio schema: (id , station , name , type , logo)
#    id is an integer primary key
#    station is the station URL
#    name is the station name (which is used as the root of the .pls
#      and .jpg files, but see also logo)
#    type is 'u' for user-defined or 's' for system-defined 
#    logo is a filepath or 'local'; user-defined stations appear
#    always to have logo='local' 

# select every row with type='u'

radios=[]
for row in conn.execute("SELECT * FROM cfg_radio WHERE type='u'"):
  # convert from tuple to dict for better visibility in json file 
  # strip id at same time; it's irrelevant for exchange purposes
  radios.append({'station':row[1],'name':row[2],'type':row[3],'logo':row[4]})

if not radios:
  print('Oops, no user-defined stations were found')
  sys.exit()

# use tmprootdir as context manager
with tempfile.TemporaryDirectory() as tmprootdir:
  RADIOdest=tmprootdir+'/RADIO/'
  logodest=tmprootdir+'/logos/'
  thumbdest=logodest+'thumbs/'
  os.mkdir(RADIOdest)
  os.mkdir(logodest)
  os.mkdir(thumbdest)

  # save the radios.json file
  datafile=open(tmprootdir+'/radios.json','w')
  json.dump(radios,datafile)
  datafile.close()

  # copy the .pls and.jpg files
  rowcnt = 0
  for row in radios:
    name = row['name']
    RADIOfile = RADIOsrc+name+'.pls'
    if not os.path.isfile(RADIOfile):
      # this shouldn't happen, but just in case
      print("skipping cfg_radio entry with name= '{}', no corresponding .pls file".format(name)) 
      continue
    shutil.copy(RADIOfile, RADIOdest)
    rowcnt += 1
    logofile = logosrc+name+'.jpg'
    thumbfile = thumbsrc+name+'.jpg'
    if os.path.isfile(logofile):
      shutil.copy(logofile,logodest)
    if os.path.isfile(thumbfile):
      shutil.copy(thumbfile,thumbdest)
  # don't break current context until this file is written
  if rowcnt > 0:
    shutil.make_archive('myradios','gztar',tmprootdir)
    print("{} station(s) saved".format(rowcnt))
    print("'tar tf myradios.tar.gz' to see its contents")
  else:
    print("No stations saved; no file written")

# note that temporary directory is removed when the context is
# exited we we don't have to.
