# Tools to save and load user-defined radio stations in moOde

The files in this repo are intended to aid users of recent vintage (5.x, 6.0) [moOde](http://moodeaudio.org) audio players in saving (e.g., exporting) and loading (e.g., importing) their user-defined radio stations in bulk. Possible use-cases include transferring the stations
* to a player after a clean install of moOde
* between moOde players running the same or different moOde releases
* between moOde users

These files are not integrated into the moOde UI in any way. All operations take place on the command line of the moOde player.

## Getting the tools onto your moOde player

The easiest way to get these files is to use **git**, which is already installed in moOdeOS. From the command line of each moOde player and in a directory writeable by you (your home directory is a good choice)
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
3 station(s) saved
'tar tf myradios.tar.gz' to see its contents
```
Obviously you need to save the tar file off the current system if you intend to do a clean install of a new release. Otherwise copy or transfer it to the target moOde player. 

**loadmyradios.py** - (assumes you have cloned the moode-radio-utils repo as described above). From the command line of the target moOde player, make sure the myradios.tar.gz file is in the same directory as loadmyradios.py.

...more to come...

**myradios.tar.gz** - an example file created by savemyradios.py on a moOde 6.0.0 player. It contains all the information needed to load three stations into the player on which loadmyradios.py is run.

* Grateful Dead Live at Carousel Ballroom 1968 - a pseudo-radio station with a playlist of tracks from the 1968-02-04 concert which are streamed from the [Live Music Archive](https://archive.org/details/gd1968-02-14.sbd.douglas-cleef.2267.shnf)
* KVCU Radio 1190 University of Colorado - a [college radio station](http://www.radio1190.org/) affiliated with the University of Colorado Boulder.
* MANGORADIO - a [German Internet radio station](https://mangoradio.de/) selected at random from the [Community Radio Browser]( http://www.radio-browser.info/gui/#!/)