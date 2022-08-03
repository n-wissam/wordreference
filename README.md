# wordreference
A python script to get translations from [wordreference](https://www.wordreference.com)

this script can be imported as a module and used as an API to get wordreference translations.

# Usage:

![wr](https://user-images.githubusercontent.com/109042485/182707300-8b9170aa-c602-47cc-98ff-a5ca0b0aa260.png)

```
usage: wordreference.py [-h] [-l] [-a] [-s] DICTIONARY_CODE word

get translation from wordreference.com

positional arguments:
  DICTIONARY_CODE       dictionary code, use -l to list a list of available dictionaries
  word                  word to translate

options:
  -h, --help            show this help message and exit
  -l, --list-available-dictionaries
                        list available dictionaries and their codes
  -a, --audio           download audio files to current directory (when available)
  -s, --sentences       get only example sentences and their meaning (when available)
```

To get a list of available dictionaries and their codes:
```
python wordreference.py -l
code  :  Dictionary
-------------------
enar  :  English-Arabic
enzh  :  English-Chinese
encz  :  English-Czech
ennl  :  English-Dutch
enfr  :  English-French
ende  :  English-German
engr  :  English-Greek
enis  :  English-Icelandic
enit  :  English-Italian
enja  :  English-Japanese
enko  :  English-Korean
enpl  :  English-Polish
enpt  :  English-Portuguese
enro  :  English-Romanian
enru  :  English-Russian
enes  :  English-Spanish
ensv  :  English-Swedish
entr  :  English-Turkish
aren  :  Arabic-English
czen  :  Czech-English
deen  :  German-English
dees  :  German-Spanish
esde  :  Spanish-German
esen  :  Spanish-English
esfr  :  Spanish-French
esit  :  Spanish-Italian
espt  :  Spanish-Portuguese
fren  :  French-English
fres  :  French-Spanish
gren  :  Greek-English
isen  :  Icelandic-English
iten  :  Italian-English
ites  :  Italian-Spanish
jaen  :  Japanese-English
koen  :  Korean-English
nlen  :  Dutch-English
plen  :  Polish-English
pten  :  Portuguese-English
ptes  :  Portuguese-Spanish
roen  :  Romanian-English
ruen  :  Russian-English
sven  :  Swedish-English
tren  :  Turkish-English
zhen  :  Chinese-English
```

# importing as a module
```python
>>> import wordreference as wr
>>> translations, audio_links = wr.define_word("programmer", "enar")
>>> print(translations)
{
    1: {
        "word": "programmer n",
        "definition": "(computer: [sb] who writes programs)",
        "meanings": ["مبرمج"],
        "examples": [["The department employs four programmers to develop products."]],
    },
    2: {
        "word": "programmer n",
        "definition": "(TV, radio: [sb] who plans schedules)",
        "meanings": ["معد برامج إذاعية وتلفزيونية"],
        "examples": [
            ["BBC programmers defended their decision to air the show at 8pm."]
        ],
    },
    3: {
        "word": "computer programmer n",
        "definition": "([sb]: writes software)",
        "meanings": ["مبرمج حاسوب"],
        "examples": [
            ["I'm a computer programmer but my job title is Chief Software Developer."]
        ],
    },
}


>>> print(audio_links)
['https://www.wordreference.com/audio/en/us/us/en1068804.mp3', 'https://www.wordreference.com/audio/en/uk/general/en1068804.mp3', 'https://www.wordreference.com/audio/en/uk/rp/en1068804.mp3', 'https://www.wordreference.com/audio/en/uk/Yorkshire/en1068804-55.mp3', 'https://www.wordreference.com/audio/en/Irish/en1068804.mp3', 'https://www.wordreference.com/audio/en/scot/en1068804.mp3', 'https://www.wordreference.com/audio/en/us/south/en1068804.mp3', 'https://www.wordreference.com/audio/en/Australian/en1068804.mp3', 'https://www.wordreference.com/audio/en/Jamaica/en1068804.mp3']
```
`define_word` function takes two arguments: a word to translate and dictionary code and it returns a tuple that cantains:
- a dictionary that contains translations of the given word.
- a list of links to available audio files that contain pronunciation of the word in different accents

`wr.print_available_dictinaries()` gives a list of available dictionary codes

# API output
**Translations:**
- **word:** the word in differnt meanings and idioms
- **definition:** definition of the word in the source language
- **meanings:** a list of meanings of the word in the target language
- **examples:** a list of exmaple sentences in the source language and tranlsations when available (sometimes multiple translations of the same sentence are included). Every sentence and its translations are stored in a list os `examples` is a list of lists

**Pronunciation:**
- list of links to audio files that contains pronunciation
# Notes
- this script requires `requests` and `Beautiful Soup` to work
- this script uses `Beautiful Soup` to scrape data from [wordreference](https://www.wordreference.com) so it may not work in future if they change things on their website.
