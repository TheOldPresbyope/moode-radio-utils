# Tools to save and load user-defined radio stations in moOde

The files in this repo are intended to aid users of recent vintage [moOde](http://moodeaudio.org) audio players in saving (e.g., exporting) and loading (e.g., importing) their user-defined radio stations in bulk.

v2.0 - Tested with moOde 6.7.1. Should work with moOde 6.6.0 and 6.7.0 as well. Should continue to work with later releases until there is another change in the moOde database schema for the cfg_radio table or the locations of the various radio directory files. Not compatible with prior releases of moOde or with myfiles.tar.gz files created using v1.0.

v1.0 - Deprecated. Tested in moOde 5.3.1 (Raspbian Stretch) and moOde 6.0.0 (Raspbian Buster). Should work with moOde releases up to 6.5.2. Not compatible with later releases nor with myfiles.tar.gz files created with v2.0.

Possible use-cases include transferring the stations
* into a freshly installed moOde player
* between moOde players running the same or different, compatible moOde releases
* between moOde users

Existing user-defined stations on the destination player are left untouched and stations to be loaded which match existing ones in name are skipped.

These files are not integrated into the moOde UI in any way. All operations take place on the command line of the moOde player.

### A note about user-defined radio stations

To be recognized by these scripts, a user-defined radio station must have at least two components:

* an entry in the cfg_radio table of the moOde database, /var/local/www/db/moode-sqlite3.db
* a corresponding .pls file in the MPD directory /var/lib/mpd/music/Radio

Optionally, it may also have a .jpg file of the station logo in /var/local/www/imagesw/radio-logos and a .jpg file of the thumbnail generated from it in /var/local/www/imagesw/radio-logos/thumbs

All these components are generated when a user clicks on the "+" icon in the Radio Directory and fills in information in the New Station menu which appears.

<b>These scripts ignore .pls files and .jpg files for which there is no corresponding entry in the database</b>

## Getting the tools onto your moOde player

The easiest way to get these files is to use **git**, which is already installed in moOdeOS. From the command line of each moOde player in a directory writeable by you (your home directory is a good choice)
```
git clone https://github.com/TheOldPresbyope/moode-radio-utils.git
cd moode-radio-utils
```
and there you are.

## How to use

**savemyradios.py** - From the command line of the source moOde player, either invoke this script as an argument to Python3 (not Python2!) or make sure it is marked executable and then invoke it directly, e.g.,
```
option (1)
python3 savemyradios.py

option (2)
chmod +x savemyradios.py
./savemyradios.py
```

The script creates ***myradios.tar.gz*** in the current working directory. Here's three examples of the CLI dialogue:
```
(a) user-defined radio stations are found

pi@moode:~ $ ./savemyradios.py
Save user-defined radio stations to 'myradios.tar.gz' in the
current working directory, overwriting existing file if present
Proceed? (y/n): y
2 station(s) saved
'tar tf myradios.tar.gz' to see its contents

(b) no user-defined radio station is found in the database

pi@moodeLR:~ $ ./savemyradios.py
Save user-defined radio stations to 'myradios.tar.gz' in the
current working directory, overwriting existing file if present
Proceed? (y/n): y
Oops, no user-defined stations were found

(c) a user-defined radio station is found in the database
    but corresponding .pls file is not found; no other
    user-defined radio station is found

pi@moode:~ $ ./savemyradios.py
Save user-defined radio stations to 'myradios.tar.gz' in the
current working directory, overwriting existing file if present
Proceed? (y/n): y
skipping cfg_radio entry with name= 'test station', no corresponding .pls file
No stations saved; no file written
```
Obviously you need to save the tar file off the current system if you intend to do a clean (re)install. To use, copy it to the destination moOde player.

**loadmyradios.py** - On the destination moOde player, ensure the myradios.tar.gz file is in the same directory as loadmyradios.py and from the command line invoke the script as superuser (required because of moOde directory permissions). As above this can be done several ways
```
option (1)
sudo python3 loadmyradios.py

option (2)
chmod +x loadmyradios.py
sudo ./loadmyradios.py
```
Once the script has run, refresh the moOde Radio Directory (click the circular arrow in the upper-left of the UI) to see the new entries.

Here's an example of the CLI dialogue (using the myradios.tar.gz file in this repo):
```
pi@moode:~/ $ sudo ./loadmyradios.py
Load user-defined radio stations from myradios.tar.gz  in the current working directory
Proceed? (y/n): y
adding station 'Grateful Dead Live at Carousel Ballroom - 1968'
1 station(s) loaded

```

**myradios.tar.gz** - an example file created by savemyradios.py on a moOde 6.7.1 player. It contains the data and image files needed to load a station into the player on which loadmyradios.py is run. The station is:

* Grateful Dead Live at Carousel Ballroom 1968 - a pseudo-radio station with a playlist of tracks from the 1968-02-04 concert. The tracks are streamed from the [Live Music Archive](https://archive.org/details/gd1968-02-14.sbd.douglas-cleef.2267.shnf) *NOTE - this "station" was chosen to show it is technically possible for moOde to stream music from the Live Music Archive. The station logo will not display in the Playback panel while playing these tracks. This is an issue I haven't resolved with moOde and imported .m3u playlists, not with the tools in this repo.*

**TODO**
* The scripts are hardwired to write/read myfiles.tar.gz. It would be nice to allow the user to specify a name.
* The scripts batch save/load all the user-defined radio stations. It would be nice to allow the user to specify the stations to be saved or at least the ones to be loaded.
* There is a modicum of error checking in the scripts but they are hardly bulletproof. It would be nice to cover more bases.
* The scripts are basically procedural code. It would be nice to make them more Pythonic.
* None of these is likely to be addressed.
