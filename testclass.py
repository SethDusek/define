import requests
from os import system
from time import time
class dict:
    def __init__(self,key,urbankey,tkey):
        self.key = key
        self.urbankey = urbankey
        self.tkey = tkey
    def getDefinition(self,word):
        definition = requests.get("http://api.wordnik.com/v4/word.json/%s/definitions?api_key=%s" % (word,self.key)).json()[0]["text"]
        return definition
    def getHyphenation(self,word):
        hyphenation = requests.get("http://api.wordnik.com/v4/word.json/%s/hyphenation?api_key=%s" % (word,self.key)).json()
        return hyphenation
    def getAudio(self,word):
        url = requests.get("http://api.wordnik.com/v4/word.json/%s/audio?api_key=%s" % (word,self.key)).json()[0]["fileUrl"]
        return requests.get(url)
    def getUrban(self,word):
        urb = requests.get("https://mashape-community-urban-dictionary.p.mashape.com/define?term=%s"
        % word, headers={"X-Mashape-Key": self.urbankey}).json()
        if urb["list"]>0:
            return urb["list"][0]["definition"]
    def getThesaurus(self,word):
        response = requests.get("http://words.bighugelabs.com/api/2/%s/%s/json"
                            % (self.tkey, word)).json()
        return response

t = dict("1e940957819058fe3ec7c59d43c09504b400110db7faa0509","ub2JDDg9Iumsh1HfdO3a3HQbZi0up1qe8LkjsnWQvyVvQLFn1q","e415520c671c26518df498d8f4736cac")
tim = time()
print(t.getDefinition("test"))
print(t.getHyphenation("test"))
#print(t.getUrban("DAE"))
#print(t.getThesaurus("test")["noun"])
aud = t.getAudio("love")
buff = open("/tmp/filename.mp3","w")
buff.write(aud.content)
buff.close()
system("gst-launch-1.0 playbin uri=file:///tmp/filename.mp3 -q")
print(time()-tim)
