#! /usr/bin/env pypy
#import wordnik # this is one weird library, importing it using import wordnik doesnt work
from wordnik import swagger,WordApi
from sys import argv
import optparse
from os import system,remove
import wget
arg = optparse.OptionParser()
arg.add_option("-a","--audio",action="store_true",default=False)
opts,rem = arg.parse_args(argv)
#print(opts)
audio = opts.audio
#print(audio)
#print(rem)
key = "1e940957819058fe3ec7c59d43c09504b400110db7faa0509" 
client = swagger.ApiClient(key,"http://api.wordnik.com/v4")
client = WordApi.WordApi(client)
for i in range(1,len(rem)):
    #wget.download(client.getAudio(rem[i])[0].fileUrl)
    print(rem[i].upper() + ": \n" + client.getDefinitions(rem[i])[0].text)
    #"\nEXAMPLE: \n"+ client.getTopExample(rem[i]).text wordnik examples are horrendous so screw them
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

