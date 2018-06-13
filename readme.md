# Yugioh Cards

Easily download and organize all Yugioh cards

## Usage

If building from source isn't your thing, there's a binary version (only windows right now) downloadable from the releases page.

Otherwise, simply get the latest version of python (tested on 3) and you'll be good to go.

From here, run the script and cards should start downloading. Note that cards will save in a folder called yugiohcards in the apps execution directory, and editionally, 2 files called cards.cdb and strings.conf will be created in the same directory as well. It may be a good idea to run from an isolated directory to avoid cludder

## languages

The main language that this app can process is english. However, because the ygopro2 database has several translated card databases, yugiohcards has a VERY buggy and VERY untested ability to use other languages supported by the ygopro2 database. Tipically, however, switching to another language will most likely cause no end of encoding errors and will break the database that yugiohcards prints.

If you wish to attempt using this support, however, feel free to modify the language variable at the top of the python script before running. Support for other languages is currently not available in the windows binary.

## Contributing

Contributions and pull requests are appreciated. If you encounter a problem, use the issue tracker.

## Credits

Script written by:

[Carter Temm](http://github.com/cartertemm)
and
[Sam Tupy](http://github.com/samtupy)