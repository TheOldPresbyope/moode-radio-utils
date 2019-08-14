# Tools to save and load user-defined radio stations in moOde

The files in this repo are intended to aid users of recent vintage [moOde](http://moodeaudio.org) audio players in saving (e.g., exporting) and loading (e.g., importing) their user-defined radio stations in bulk. They have been tested in moOde 5.3.1 (Raspbian Stretch) and moOde 6.0.0 (Raspbian Buster). 

Possible use-cases include transferring the stations
* into a freshly installed moOde player
* between moOde players running the same or different moOde releases
* between moOde users

Existing user-defined stations on the destination player are left untouched and stations to be loaded which match existing ones in name are skipped.

These files are not integrated into the moOde UI in any way. All operations take place on the command line of the moOde player.

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

The script creates ***myradios.tar.gz*** in the current working directory. Here's an example of the CLI dialogue:
```pi@moode:~/ $ ./savemyradios.py
Save user-defined radio stations to 'myradios.tar.gz' in the
current working directory, overwriting existing file if present
Proceed? (y/n): y
2 station(s) saved
'tar tf myradios.tar.gz' to see its contents
```
Obviously you need to save the tar file off the current system if you intend to do a clean (re)install. Copy or transfer it to the destination moOde player.

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
adding station 'MANGORADIO'
2 station(s) loaded

```

**myradios.tar.gz** - an example file created by savemyradios.py on a moOde 6.0.0 player. It contains the data and image files needed to load two stations into the player on which loadmyradios.py is run.

* Grateful Dead Live at Carousel Ballroom 1968 - a pseudo-radio station with a playlist of tracks from the 1968-02-04 concert. The tracks are streamed from the [Live Music Archive](https://archive.org/details/gd1968-02-14.sbd.douglas-cleef.2267.shnf)
* MANGORADIO - a [German Internet radio station](https://mangoradio.de/) selected at random from the [Community Radio Browser]( http://www.radio-browser.info/gui/#!/)

**TODO**
* The scripts are hardwired to write/read myfiles.tar.gz. It would be nice to allow the user to specify a name.
* The scripts batch save/load all the user-defined radio stations. It would be nice to allow the user to specify the stations to be saved or at least the ones to be loaded.
* There is a modicum of error checking in the scripts but they are hardly bulletproof. It would be nice to cover more bases.
* The scripts are basically procedural code. It would be nice to make them more Pythonic.
* None of this is a priority for me.
