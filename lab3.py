import nltk
from pathlib import Path
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
from nltk import *
from nltk.corpus import stopwords
from string import punctuation
import tkinter as tk
import math
from gensim.summarization.summarizer import summarize
from rake_nltk import Rake

doc_name = ""
text = ""
result = ""

root=Tk()
space0 = Label(root,text='\n')
aboutButton = Button(root,text='About',width=8,height=2,bg='light grey')
space1 = Label(root,text='\n')
chooseDocButton=Button(root,text='Choose doc',width=55,height=2,bg='light grey')
space2 = Label(root,text='\n')
resultText = tk.Text(root, state='disabled', width=80, height=20)
space3 = Label(root,text='\n')
detectButton=Button(root,text='Get key words and summarize',width=55,height=2,bg='light grey')
space4 = Label(root,text='\n')
saveButton=Button(root,text='Save',width=55,height=2,bg='light grey')
space5 = Label(root,text='\n')

def nameOf(path):
    return Path(path).stem

def chooseDocsClicked():
    global doc_name, text
    resultText.delete('1.0', END)
    files = filedialog.askopenfilename(multiple=False)
    splitlist = root.tk.splitlist(files)
    for doc in splitlist:
        doc_name = nameOf(doc)
        text = Path(doc, encoding="UTF-8", errors='ignore').read_text(encoding="UTF-8", errors='ignore')

def extract_keywords_from(text):
    r = Rake(max_length=5)
    r.extract_keywords_from_text(text)
    return ', '.join(r.get_ranked_phrases()[:5])

def get_essay(text):
    sentences = []
    for sentence in nltk.sent_tokenize(text):
        terms = []
        for term in nltk.word_tokenize(sentence):
            if term not in punctuation and term not in stopwords.words('russian') and term not in stopwords.words('english'):
                terms.append(term)
        sentences.append(terms)
    scores = []
    for sentence in sentences:
        score = 0
        for term in sentence:
            score += ((sentence.count(term)/len(sentence)) * 0.5 * (1+((sentence.count(term)/len(sentence))/(max_freq(sentence))))*math.log(len(sentences)/term_count(term, sentences)))
        scores.append(score)
    essay = ""
    for _ in range(int(len(sentences)/3)):
        current_max = max(scores)
        for i in range(len(scores)-1):
            if scores[i] == current_max:
                essay += nltk.sent_tokenize(text)[i]
                scores.remove(current_max)
                break
    return essay
                      
def max_freq(sentence):
    result = 0
    for term in sentence:
        result = max(result,sentence.count(term))
    return result/len(sentence)
                      
def term_count(term, sentences):
    result = 0
    for sentence in sentences:
        if term in sentence:
            result+=1
    return result

def detectClicked():
    global result
    result = ""
    result += "--- KEY WORDS: ---\n"
    result += extract_keywords_from(text)
    result += "\n\n--- ESSAY: ---\n"
    result += get_essay(text)
    result += "\n\n--- SUMMARIZE: ---\n"
    result += summarize(text)
    resultText.configure(state='normal')
    resultText.insert('end', result)
    resultText.configure(state='disabled')

def saveClicked():
    file = open(doc_name + '_result.txt', 'w', encoding="utf8")
    file.write(result)
    file.close()

def aboutButtonClicked():
    messagebox.showinfo("Lab 3", "Usage: Choose file. Then click \"Get key words and summarize\" button.\nYou can also save result.\n\nDeveloped by: Artyom Gurbovich and Pavel Kalenik.")

aboutButton.config(command=aboutButtonClicked)
chooseDocButton.config(command=chooseDocsClicked)
detectButton.config(command=detectClicked)
saveButton.config(command=saveClicked)

space0.pack()
aboutButton.pack()
space1.pack()
chooseDocButton.pack()
space2.pack()
resultText.pack()
space3.pack()
detectButton.pack()
space4.pack()
saveButton.pack()
space5.pack()
root.mainloop()