# Tools to save and load user-defined radio stations in moOde

The files in this repo are intended to aid users of the moOde audio player in saving (e.g., exporting) and loading (e.g., importing) their user-defined radio stations in bulk. Possible use-cases include transferring the stations
* from a player running an old moOde release to the same player after a clean install of a new release
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

## <tl;dr> how to use

**savemyradios.py** - From the command line of the source moOde player, either invoke this script as an argument to Python3 (not Python2!) or make sure it is marked executable and then invoke it directly, e.g.,
```
option (1)
python3 savemyradios.py

option (2)
chmod +x savemyradios.py
./savemyradios.py
```
It will create a file ***myradios.tar.gz*** in the current working directory. Obviously you need to save it off the current system if you intend to do a clean install of a new release. Otherwise copy or transfer it to the target moOde player. 

**loadmyradios.py** - (assumes you have cloned the moode-radio-utils repo as described above). From the command line of the target moOde player. Make sure the ***myradios.tar.gz*** file is in the same directory as **loadmyradios.py**.
...more to come...

**myradios.tar.gz** - an example file created by savemyradios.py on a moOde 6.0. player. It contains all the information needed to load three stations into the player on which **loadmyradios.py** is run.

* Grateful Dead Live at Carousel Ballroom 1968 - a pseudo-radio station streaming tracks from the 1968-02-04 concert out of a [Live Music Archive](https://archive.org/details/gd1968-02-14.sbd.douglas-cleef.2267.shnf) holding
* KVCU Radio 1190 University of Colorado - a [college radio station](http://www.radio1190.org/) affiliated with the University of Colorado Boulder.
* MANGORADIO - a [German Internet radio station](https://mangoradio.de/) selected at random from the [Community Radio Browser]( http://www.radio-browser.info/gui/#!/)
