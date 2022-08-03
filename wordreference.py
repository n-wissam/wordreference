import argparse
import requests
from bs4 import BeautifulSoup

URL = "https://www.wordreference.com"

wr_available_dictinoaries = (
("enar" , "English-Arabic"),
("enzh" , "English-Chinese"),
("encz" , "English-Czech"),
("ennl" , "English-Dutch"),
("enfr" , "English-French"),
("ende" , "English-German"),
("engr" , "English-Greek"),
("enis" , "English-Icelandic"),
("enit" , "English-Italian"),
("enja" , "English-Japanese"),
("enko" , "English-Korean"),
("enpl" , "English-Polish"),
("enpt" , "English-Portuguese"),
("enro" , "English-Romanian"),
("enru" , "English-Russian"),
("enes" , "English-Spanish"),
("ensv" , "English-Swedish"),
("entr" , "English-Turkish"),
("aren" , "Arabic-English"),
("czen" , "Czech-English"),
("deen" , "German-English"),
("dees" , "German-Spanish"),
("esde" , "Spanish-German"),
("esen" , "Spanish-English"),
("esfr" , "Spanish-French"),
("esit" , "Spanish-Italian"),
("espt" , "Spanish-Portuguese"),
("fren" , "French-English"),
("fres" , "French-Spanish"),
("gren" , "Greek-English"),
("isen" , "Icelandic-English"),
("iten" , "Italian-English"),
("ites" , "Italian-Spanish"),
("jaen" , "Japanese-English"),
("koen" , "Korean-English"),
("nlen" , "Dutch-English"),
("plen" , "Polish-English"),
("pten" , "Portuguese-English"),
("ptes" , "Portuguese-Spanish"),
("roen" , "Romanian-English"),
("ruen" , "Russian-English"),
("sven" , "Swedish-English"),
("tren" , "Turkish-English"),
("zhen" , "Chinese-English"))

def print_available_dictinaries():
    print('code  :  Dictionary\n-------------------')
    for dict in wr_available_dictinoaries:
        print(dict[0]," : ", dict[1])

def define_word(word,dict_code):
    page = requests.get(URL+ '/' + dict_code + '/' + word)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("tr", {'class':['even', 'odd']})
    bad_rows = []

    for row_number in range(len(results)):
        if "more" in results[row_number]['class']:
            bad_rows.append(row_number)

    for row_number in reversed(bad_rows):
        del results[row_number]

    translations = {}
    translation_number = 0
    example = []

    for row in results:
        if (row.find(class_="FrWrd")):
            if example: translation["examples"].append(example)
            if translation_number > 0: translations[translation_number] = translation
            translation_number += 1
            example = []
            translation = {"word" : "",
                "definition" : "",
                "meanings" : [],
                "examples" : []
                }
            translation["word"] = row.td.get_text().strip().replace('⇒','').replace(u'\xa0', u' ').replace(u'\u24d8', u'')
            translation["definition"] = row.td.next_sibling.get_text().strip().replace('⇒','').replace(u'\xa0', u' ').replace(u'\u24d8', u'')
            translation["meanings"].append(row.td.next_sibling.next_sibling.get_text().strip().replace('⇒','').replace(u'\xa0', u' ').replace(u'\u24d8', u''))
        elif (row.find(class_="ToWrd")):
            to2 = ''
            if (row.find(class_="To2")):
                to2 = row.td.next_sibling.get_text().strip().replace('⇒','').replace(u'\xa0', u' ').replace(u'\u24d8', u'')
            translation["meanings"].append(row.td.next_sibling.next_sibling.get_text().strip().replace('⇒','').replace(u'\xa0', u' ').replace(u'\u24d8', u'') + to2)
        elif(row.find(class_="FrEx")):
            if example:
                translation["examples"].append(example)
            example = []
            example.append(row.td.next_sibling.get_text().strip().replace(u'\xa0', u' ').replace(u'\u24d8', u''))
        elif(row.find(class_="ToEx")):
            example.append(row.td.next_sibling.get_text().strip().replace(u'\xa0', u' ').replace(u'\u24d8', u''))
        else:
            pass
    if example:
        translation["examples"].append(example)
    if translation_number > 0:
            translations[translation_number] = translation
    
    try:
        audio_links = soup.find("div",id = "listen_widget").script.string[18:-3].split(',')
        audio_links = [URL + link[1:-1] for link in audio_links]
    except:
        audio_links = []
        
    result = (translations, audio_links)
    return result

class list_dict_codes(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        return super().__init__(option_strings, dest, nargs=0, default=argparse.SUPPRESS, **kwargs)
    
    def __call__(self, parser, namespace, values, option_string, **kwargs):
        print_available_dictinaries()
        parser.exit()

def print_translations(translations, colors=""):
    for value in translations.values():
        print ("\033[92m" + value['word'] + "\033[00m", '\t' , value['definition'])
        for meaning in value["meanings"]:
            print("\033[96m" + meaning + "\033[00m")
        for examples_list in value["examples"]:
            for example in range(len(examples_list)):
                if not example:
                    print("\033[91m" + " \u2022 " + "\033[00m" + examples_list[example])
                else:
                    print("\033[93m   " + examples_list[example] + "\033[00m")
        print('_' * 80)

def print_examples(translations):
    for value in translations.values():
        for examples_list in value["examples"]:
            for example in range(len(examples_list)):
                if not example:
                    print("\033[91m" + " \u2022 " + "\033[00m" + examples_list[example])
                else:
                    print("\033[93m   " + examples_list[example] + "\033[00m")

def download_audio(word, links):
    for audio_link in links:
        file = requests.get(audio_link)
        if file.status_code == 200:
            open(word + '-' + audio_link.rsplit('/', 2)[1] + '.mp3', 'wb').write(file.content)

def parse_arguments():
    parser = argparse.ArgumentParser(description="get translation from wordreference.com ")
    parser.add_argument("dictionary_code", help = "dictionary code, use -l to list a list of available dictionaries", choices = ["enar","enzh","encz","ennl","enfr","ende","engr","enis","enit","enja","enko","enpl","enpt","enro","enru","enes","ensv","entr","aren","czen","deen","dees","esde","esen","esfr","esit","espt","fren","fres","gren","isen","iten","ites","jaen","koen","nlen","plen","pten","ptes","roen","ruen","sven","tren","zhen"], metavar ="DICTIONARY_CODE")
    parser.add_argument("-l", "--list-available-dictionaries", help = " list available dictionaries and their codes", action = list_dict_codes)
    parser.add_argument("-a", "--audio", help = "download audio files to current directory (when available)", action='store_true')
    parser.add_argument("-s", "--sentences", help = "get only example sentences and their meaning (when available)", action='store_true')
    parser.add_argument("word", help = "word to translate")
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    translations,audio_links = define_word(args.word, args.dictionary_code)
    if args.sentences:
        print_examples(translations)
    else:
        print_translations(translations)

    
    if args.audio and not audio_links:
        print("No audio files for this word")
    if args.audio and audio_links:
        print("downloading audio files")
        download_audio(args.word, audio_links)
        print("finished downloading audio files")
    
if __name__ == '__main__':
    main()