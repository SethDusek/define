#!/usr/bin/python
import sys
from sys import argv
import optparse
from os import system
from os import path
import requests
import subprocess
import re
try:
    from .__version__ import __version__
except ValueError:
    from __version__ import __version__
except SystemError:
    from __version__ import __version__

regex = re.compile("^\d\.")
key = "1e940957819058fe3ec7c59d43c09504b400110db7faa0509"
tkey = "e415520c671c26518df498d8f4736cac"
urbankey = "ub2JDDg9Iumsh1HfdO3a3HQbZi0up1qe8LkjsnWQvyVvQLFn1q"
hyphenation = False  # Disable or Enable Hyphenation
try:
    raw_input_ = raw_input
except NameError:
    raw_input_ = input

max_definitions = 3


class dict:

    def __init__(self, key, urbankey, tkey):
        self.key = key
        self.urbankey = urbankey
        self.tkey = tkey

    def getDefinition(self, word, source="all"):
        definition = requests.get(
            "http://api.wordnik.com/v4/word.json/%s/definitions?limit=%s"
            "&api_key=%s&caseSensitive=false&useCanonical=true&"
            "sourceDictionaries=%s" % (word, max_definitions, self.key,
                                       source)).json()
        if len(definition) >= 1:
            try:
                return definition
            except TypeError:
                raise
            else:
                raise

    def getHyphenation(self, word):
        hyphenation = requests.get(
            "http://api.wordnik.com/v4/word.json/%s/hyphenation?api_key=%s"
            % (word, self.key)).json()
        return hyphenation

    def getAudio(self, word):
        url = requests.get("http://api.wordnik.com/v4/word.json/%s/audio?"
                           "api_key=%s" % (word, self.key)).json()
        if len(url) >= 1:
            url = url[0]["fileUrl"]
        else:
            return False, "", ""
        return True, url, requests.get(url)

    def getUrban(self, word):
        try:
            urb = requests.get("https://mashape-community-urban-dictionary.p."
                               "mashape.com/define?term=%s"
                               % word, headers={"X-Mashape-Key":
                                                self.urbankey}).json()
        except requests.exceptions.SSLError:
            urb = requests.get("https://mashape-community-urban-dictionary.p."
                               "mashape.com/define?term={0}",
                               verify="/etc/ssl/certs/ca-certificates.crt",
                               headers={"X-Mashape-Key":
                                        self.urbankey}).json()
        if len(urb["list"]) > 0:
            return urb["list"][0]["definition"]

    def getThesaurus(self, word):
        """response = requests.get("http://words.bighugelabs.com/api/2/%s/%s/json"
                            % (self.tkey, word)).json()
        return response"""
        response = requests.get(
            "http://api.wordnik.com:80/v4/word.json/%s/relatedWords?"
            "useCanonical=false&relationshipTypes=synonym&limitPer"
            "RelationshipType=15&api_key=%s" % (word, key)).json()
        try:
            return response[0]
        except IndexError:
            pass


# credit to
# http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
    import os

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for pathh in os.environ["PATH"].split(os.pathsep):
            pathh = pathh.strip('"')
            exe_file = os.path.join(pathh, program)
            if is_exe(exe_file):
                return exe_file

    return None


def parse_hunspell(word):
    if which("hunspell"):
        hunspell = subprocess.Popen("hunspell", stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
        try:
            output = hunspell.communicate(input=bytes(word, "utf-8"))[0]
        except TypeError:
            output = hunspell.communicate(input=word)[0]
        try:
            words = output.decode().split(": ")[1].split(", ")
        except IndexError:
            words = output.decode().split(": ")[0].split(", ")
        words = [v.rstrip() for v in words]
        return {"word": word, "suggestions": words}
    else:
        return requests.get("http://i.shibe.ml:8080?word=%s" % word).json()[0]


def getLocalWordnet(word):
    definitions = []
    output = subprocess.Popen(["wn", word, "-over"],
                              stdout=subprocess.PIPE).communicate()[0]
    for line in output.split("\n"):
        reg = regex.search(line)
        if reg:
            definitions.append(line[reg.end():].split("--")[1]
                               [2:len(line.split("--")[1]) - 1].split(";")[0])
    return definitions
wn_exists = False
if which("wn"):
    wn_exists = True
""" Returns the options that the user
defined as well as the actual argument defined"""


def get_args():
    arg = optparse.OptionParser(version='%prog ' + __version__)
    arg.add_option("-a", "--audio", action="store_true",
                   help='audio playback for the the search result',
                   default=False)
    arg.add_option("-t", "--thesaurus", action="store_true",
                   help='show search results using thesaurus', default=False)
    arg.add_option("-u", "--urban", action="store_true",
                   help='show search results using urbandictionary.com',
                   default=False)
    arg.add_option("-w", "--wordnet", action="store_true",
                   help='show search results using wordnet')
    arg.add_option("-l", "--local", action="store_true",
                   help='show search results using local dict and dictd',
                   default=False)
    arg.add_option("-k", "--wiktionary", action="store_true",
                   help='show search results using wiktionary')
    return arg.parse_args(argv)


def check_args_valid(required_args):
    if len(required_args) == 1:
        print("usage: define [options]\
        \n-a, --audio Audio pronunciations\
        \n-t, --thesaurus Thesaurus\
        \n-u, --urban, Search Urban Dictionary instead of Wordnik\
        \n-h, --help, Display help and exit")
        sys.exit()


def get_wordapi_client():
    return dict(key, urbankey, tkey)


def play_definition(word, client):
    ask = raw_input_("\nWould you like to hear audio pronunciation? [y/N] ")

    if ask.lower().startswith("y"):
        valid, url, obj = client.getAudio(word)
        if valid is False:
            print("Couldn't get Audio")
            return
        # filen = wget.download(url,"/tmp")
        down = obj.content
        filen = url.split("/")[5]
        buff = open("/tmp/%s" % filen, "wb")
        buff.write(down)
        buff.close()
        system("gst-launch-1.0 playbin uri=file:///tmp/%s -q" % filen)
        while True:
            ask = raw_input_("\nWould you like to hear it again? [y/N] ")
            if ask.lower().startswith("y"):
                system("gst-launch-1.0 -q playbin uri=file:///tmp/%s" % filen)
            else:
                break


def print_urban_dictionary_definition(word, client):
    urb = client.getUrban(word)
    if urb:
        print(client.getUrban(word))
    else:
        print("Couldn't get definition from urbandictionary.com")


def print_wordnik_definition(word, client, source="all"):
    try:
        cons = []
        if hyphenation:
            for i in client.getHyphenation(word):
                cons.append(i["text"])
        definition = client.getDefinition(word, source)
        if definition is None:
            print("Did you mean: " +
                  ",".join(parse_hunspell(word)["suggestions"]))
        else:
            if len(definition) == 1:
                print(definition[0]["text"])
            elif len(definition) > 1:
                for i, v in enumerate(definition):
                    print("%s. %s" % (i + 1, v["text"]))
    except requests.exceptions.ConnectionError:
        if which("dict") is not None:
            fallback = raw_input_(
                "There was a connection error, but dict was detected. \
                        Would you like to use dict? [y/N] ")
            if fallback.lower().startswith("y"):
                definitions = getLocalDefinition(word)
                if len(definitions) >= 1:
                    print(definitions[0])
            else:
                pass
    except:
        print("Not found")
        print("Did you mean: " + ",".join(parse_hunspell(word)["suggestions"]))


def getLocalDefinition(word):
    definitions = []
    output = subprocess.Popen(["dict", word], stdout=subprocess.PIPE)
    output = output.communicate()[0]
    try:
        lines = str(output, encoding="utf-8").split("\n")
    except TypeError:  # screw you python3
        lines = output.split("\n")
    for i, v in enumerate(lines):
        if v.startswith("     "):
            if v[5].isdigit():
                endline = None
                for a, b in enumerate(lines[i:]):
                    if b.startswith("        ["):
                        endline = a + i
                        definitions.append(" ".join(lines[i:endline])
                                           .replace("        ", "")[8:])
                        # print(lines[i:endline])
                        break
    return definitions


def getWordnet(word):
    definitions = word(word).definitions
    if len(definitions) >= 1:
        return definitions[0]


def getLocalAudio(word):
    ask = raw_input_("\nWould you like to hear audio pronunciation? [y/N] ")
    if ask.lower().startswith("y"):
        system("espeak %s" % word)
    else:
        pass
    while True:
        ask = raw_input_("\nWould you like to hear it again? [y/N] ")
        if ask.lower().startswith("y"):
            system("espeak %s" % word)
        else:
            break


def print_thesaurus_response(word, client):
    response = client.getThesaurus(word)
    print("SYNONYMS: ")
    """if "noun" in response:
        print("\nNouns:\n%s" % " ".join(response["noun"]["syn"]))
    if "verb" in response:
        print("Verbs:\n%s" % " ".join(response["verb"]["syn"]))"""
    try:
        print(",".join(response["words"]))
    except TypeError:
        pass


""" Given a list of words, this function will
write their respective definitions on the terminal."""


def print_each_definition(words, client, optional_args):
    audio = optional_args.audio
    thesaurus = optional_args.thesaurus
    urban = optional_args.urban
    local = optional_args.local
    wordnet = optional_args.wordnet
    wiktionary = optional_args.wiktionary
    for word in words[1:]:
        print(word.upper() + ":")
        if urban:
            print_urban_dictionary_definition(word, client)
        elif wordnet:
            if wn_exists:
                print(getLocalWordnet(word)[0])
            else:
                print_wordnik_definition(word, client, "wordnet")
        elif local:
            try:
                print(getLocalDefinition(word)[0])
            except IndexError:
                print("Definition Not Found")
            except OSError:
                print("The program dict could not be found.")
        elif wiktionary:
            print_wordnik_definition(word, client, "wiktionary")
        else:
            print_wordnik_definition(word, client)
        if thesaurus:
            print_thesaurus_response(word, client)
        if audio and local and which("espeak"):
            getLocalAudio(word)
        elif audio:
            play_definition(word, client)


def main():
    (optional_args, required_args) = get_args()
    check_args_valid(required_args)
    client = get_wordapi_client()
    print_each_definition(required_args, client, optional_args)

if __name__ == "__main__":
    if __package__ is None:
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    else:
        pass
    main()
