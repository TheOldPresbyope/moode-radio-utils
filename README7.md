# Transferring user-defined radio stations from a moOde 6.7.1 player to a moOde 7.0.0 player

A new loadmyradios7.py script has been created for this sole purpose. To use it, take these steps:

1. On the moOde r6.7.1 player
   * either run the `git clone` procedure as described in the original README or simply download the savemyradios.py script from this repo
   * in the same manner as described in the original README, run the savemyradios.py script and save off the resulting myradios.tar.gz file.
1. On the target moOde 7.0.0 player
   * install the Python Imaging Library package
      ```
      sudo apt install python3-pil
      ```
   * get the loadmyradios7.py script either by running the `git clone` procedure as described in the original README or simply download the loadmyradios7.py script from this repo
   * copy in the myradios.tar.gz file (created in step 1) to the directory containing the loadmyradios7.py script
   * in the same manner as described in the README for using loadmyradios.py, run loadmyradios7.py as superuser, for example
      ```
      sudo python3 loadmyradios7.py
      ```
   * finally, it may be necessary to refresh the Library Radio view in the moOde player
