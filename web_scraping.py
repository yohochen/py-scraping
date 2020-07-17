import requests
import string
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from bs4.element import Comment
from IPython.display import clear_output

def filterWaste(word):
    word = word.lower()
    bad_words = ('the', 'a', 'in', 'of', 'to', 'you', '\xa0', 'and', 'at', 'on', 'for', 'from', 'is', 'that', 'are', 'be', '-', 'as', '&', 'they', 'with',
                 'how', 'was', 'her', 'him', 'i', 'has', '|', 'his')

    if word in bad_words:
        return False
    elif word in string.punctuation:
        return False
    elif word.isdigit():
        return False
    else:
        return True

def filterTags(element):
    if element.parent.name in ["style", "script", "head", "title", "meta", "[document]"]:
        return False
    if isinstance(element, Comment):
        return False
    return True

def scrape(site):
    page = requests.get(site)
    soup = BeautifulSoup(page.content, "html.parser")
    text = soup.find_all(text=True)
    visible_text = filter(filterTags, text)
    word_count = {}
    for text in visible_text:
        words = text.replace('\r', '').replace('\n', '').replace('\t', '').split(' ')   # replace all hidden chars
        words = list(filter(filterWaste, words))

        for word in words:
            if word != '':
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1

    word_count = sorted(word_count.items(), key=lambda kv:kv[1], reverse=True)
    return word_count[:10]


while input("Would you like to scrape a website (y/n)? ") == "y":
    try:
        clear_output()
        site = input("Enter a website to analyze: ")
        top_words = scrape(site)
        top_word = top_words[0]
        print("The top word is: {}".format(top_word[0]))
        print(top_words)
#         displayResults(top_words, site)
    except:
        print("Something went wrong, please try again.")
print("Thanks for analyzing! Come back again!")
