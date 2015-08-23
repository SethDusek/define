#WhatIs

WhatIs is a terminal dictionary script that uses wordnik for definitions. Supports audio pronounciation

Example:

>$whatis love

>LOVE: 

>A deep, tender, ineffable feeling of affection and solicitude toward a person, such as that arising from kinship, recognition of attractive qualities, or a sense of underlying oneness.

#INSTALLATION
Installing whatis is easy, rename it to whatis and move it to /usr/bin.

Dependencies can be installed using this command:

>$ sudo pip install wordnik wget


~~You will need an api key from wordnik, get one from developer.wordnik.com and edit the "key" variable inside the script~~ *API key is now included in the script"

#Using Audio

Audio can be used in whatis with the -a or --audio flag.

>$ whatis --audio love

>LOVE: 

>A deep, tender, ineffable feeling of affection and solicitude toward a person, such as that arising from kinship, recognition of attractive qualities, or a sense of underlying oneness.

>Would you like to hear audio pronounciation? [Y/N] n

