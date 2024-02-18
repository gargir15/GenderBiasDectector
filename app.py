from flask import Flask, render_template, request
import string
import nltk
from nltk.corpus import stopwords

app = Flask(__name__)

@app.route("/")
@app.route("/home")

def home():
    return render_template("index.html")


@app.route("/result", methods = ['POST', 'GET'])
def result():
    if request.method == "POST":
        text_input = request.form['text_input']
        result = detect(text_input)
        return render_template("index.html", result=result)
    else:
        return render_template("index.html")
    
def detect(text):
    #this is the list of keywords we are using to check for bias
    keywords = ["mankind", "manpower", "man", "fathering", "mothering", "fireman", "policeman", "postman", "chairman", "chairwoman", "his", "her", "anchorman", "anchorwoman", "clergyman", "congressman"]

    count_biased = 0
    non_count = 0

    #takes punctuation out of inputted sentence
    new_text = ""
    for i in text:
        if i not in string.punctuation:
            new_text = new_text + i

    word_tokens = nltk.word_tokenize(new_text) #tokenizes the sentence (splits into words)
    stop_words = set(stopwords.words("english")) #there is already a set list of certain stop words (and, the, or, etc)


    #if a word isn't a stop word, it will add it to a new list
    for word in word_tokens: 
        if word.lower() not in stop_words: 
            non_count += 1
            if word.lower() in keywords:
                count_biased += 1


    ratio = (count_biased / non_count) * 100
    print(ratio)

    return str(round(ratio, 2))

if __name__ == '__main__':
    app.run(debug=True,port=5001)