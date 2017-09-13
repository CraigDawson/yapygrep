# yapygrep

A Python 3 file grepper like UniversalCodeGrep [ucg](https://github.com/gvansickle/ucg) or ripgrep and a silly test

## Design
* Overview
    * Text GUI with graphical options
    * Multiprocessor
    * Regex
    * Dir/File tree searching

* PyQt5 GUI
    * if cmdline argst then GUI pops-up and search runs (-g) else GUI starts and waits for user input

* Usage
    * yapygrep [switches] pattern [files/dirs]
    
* Switches (ripgrep/ucg like)
    * --gui=yes/no switch??
    * -g  => Go (run right away)
    * -t py => Type of files to look for

## Modules
* regex

## Interpreter
* [pypy](https://pypy.org) if it works in PyQt5

