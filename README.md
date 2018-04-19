# yapygrep

A Python 3 file grepper like UniversalCodeGrep [ucg](https://github.com/gvansickle/ucg) or [ripgrep](https://github.com/BurntSushi/ripgrep)

## Design
* Overview
    * Text GUI with graphical options
    * Multiprocessor  -- Craig
    * Regex  -- Peter
    * Dir/File tree searching -- Kevin

* [PyQt5](https://www.riverbankcomputing.com/news) GUI
    * if cmdline argst then GUI pops-up and search runs (-g) else GUI starts and waits for user input

* Usage
    * yapygrep [switches] pattern [files/dirs ...]
    
* Switches (ripgrep/ucg like)
    * --gui=yes/no switch??
    * -g       Go (run right away)
    * -t FTYPE Type of files to look for
    * -r       Recurse (default)
    * -n       No recurse
    * -h       Help

## Modules
* regex

## Interpreter
* [pypy](https://pypy.org) if it works in PyQt5

