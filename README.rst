Define
======

Define is a terminal dictionary script that uses wordnik for
definitions. Supports audio pronounciation

Example:

    $define love

    LOVE:

    A deep, tender, ineffable feeling of affection and solicitude toward
    a person, such as that arising from kinship, recognition of
    attractive qualities, or a sense of underlying oneness.

INSTALLATION
============

Installing define is easy:

Using pip:

    $ sudo pip install define

On Arch:

    $ yaourt -S define

Manual Installation:

    $ sudo python setup.py install
~~You will need an api key from wordnik, get one from
developer.wordnik.com and edit the "key" variable inside the script~~
\*API key is now included in the script"

Notes for Ubuntu 15.04 (may apply to other versions):
    To enable pip you'll need to add universe to your sources.

    $ echo "deb http://archive.ubuntu.com/ubuntu/ vivid universe" | sudo tee -a "/etc/apt/sources.list"

    $ sudo apt-get update

    $ sudo apt-get install python-pip

    To make use of audio feature if you install with pip. You'll need to install the gstreamer pacakge.

    $ sudo apt-get install gstreamer1.0-tools

Using Audio
===========

Audio can be used in define with the -a or --audio flag.

    $ define --audio love

    LOVE:

    A deep, tender, ineffable feeling of affection and solicitude toward
    a person, such as that arising from kinship, recognition of
    attractive qualities, or a sense of underlying oneness.

    Would you like to hear audio pronounciation? [Y/N] n

FLAGS
=====

Define has the following flags:

*-h/--help* - Display help and exit.

*-a/--audio* - Audio pronounciation of keyword.

*-t/--thesaurus* - Thesaurus results for keyword.

*-u/--urban* - Search Urban Dictionary for results instead of Wordnik.

*-l/--local* - Search keywords using local dict and dictd dictionary (NOTE: This currently only works with the gcide dictionary, no other dictionary will work at the moment)

