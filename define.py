#! /usr/bin/env python
#import wordnik # this is one weird library, importing it using import wordnik doesnt work
from wordnik import swagger,WordApi
from sys import argv
import optparse
from os import system,remove
import wget
import requests
arg = optparse.OptionParser()
arg.add_option("-a","--audio",action="store_true",default=False)
arg.add_option("-t","--thesaurus",action="store_true",default=False)
opts,rem = arg.parse_args(argv)
#print(opts)
audio = opts.audio
thesaurus = opts.thesaurus
#print(audio)
#print(rem)
key = "1e940957819058fe3ec7c59d43c09504b400110db7faa0509"
tkey = "e415520c671c26518df498d8f4736cac" #thesaurus key
client = swagger.ApiClient(key,"http://api.wordnik.com/v4")
client = WordApi.WordApi(client)
for i in range(1,len(rem)):
    #wget.download(client.getAudio(rem[i])[0].fileUrl)
    print(rem[i].upper() + ": \n" + client.getDefinitions(rem[i])[0].text)
    #"\nEXAMPLE: \n"+ client.getTopExample(rem[i]).text wordnik examples are horrendous so screw them
    if thesaurus:
        thes = requests.get("http://words.bighugelabs.com/api/2/%s/%s/json" % (tkey,rem[i])).json()
        print("SYNONYMS: ")
        if "noun" in thes:
            print("\nNouns: %s" % " ".join(thes["noun"]["syn"]))
        if "verb" in thes:
            print("Verbs: %s" % " ".join(thes["verb"]["syn"]))
    if audio:
        pass
        ask = raw_input("Would you like to hear audio pronounciation? [Y/N] ")
        if ask.lower().startswith("y"):
            url = client.getAudio(rem[i])[0].fileUrl
            filen = wget.download(url,"/tmp")
            print(url)
            system("play -t mp3 -q %s" % filen)
            while True:
                ask = raw_input("Would you like to hear it again? [Y/N] ")
                if ask.lower().startswith("y"):
                    system("play -t mp3 -q %s" % filen)
                else:
                    break
        else:
            pass

