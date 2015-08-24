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

Installing define is easy, just clone it and run:
    $ sudo python setup.py install


On Arch you can do this to install all dependencies and the program:

    $ sudo yaourt -S define-git

[STRIKEOUT:You will need an api key from wordnik, get one from
developer.wordnik.com and edit the "key" variable inside the script]
\*API key is now included in the script"

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

*-a/--audio* - Audio pronounciation

*-t/--thesaurus* - Thesaurus
*-u/--urban* - Search Urban Dictionary instead of Wordnik
