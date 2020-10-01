import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import main_functions
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from pprint import pprint
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#nltk.download("punkt")
#nltk.download("stopwords")

api_key_dict = main_functions.read_from_file("JSON_File/api_key.json")      # Assigns api_key_dict with the value that
                                                                            # read_from_file method will return from
                                                                            # the main_functions

api_key = api_key_dict["my_key"]                                            # Assigns api_key with the value inside of
                                                                            # json file that has the keyword "my_key"

st.title("COP4813 - Web Application Programming")                           # Displays a title

st.title("Project 1")                                                       # Displays a title

st.header("Part A - The Stories API")                                       # Displays a header

st.write("This app uses the Top Stories API to display the most common words used in the top current"
" articles based on a specific topic selected by the user. The data is displayed as a line chart and"
" as a wordcloud image.")

st.subheader("I - Topic Selection")                                         # Displays a subheader

name = st.text_input("Please enter your name")                              # Assigns name with the text input value

topic_of_interest = st.selectbox("Select a topic of your interest",         # Assigns topic_of_interest with the select
                 ["", "arts", "automobiles", "books", "business",           # box value
                  "fashion", "food", "health", "home", "insider",
                  "magazine", "movies", "nyregion", "obituaries",
                  "opinion", "politics", "realestate", "science",
                  "sports", "sundayreview", "technology", "theater",
                  "t-magazine", "travel", "upshot", "us", "world"])

if st.text_input and st.selectbox and name is not "" \
        and topic_of_interest is not "":                                    # If the text_input has a value and name is
                                                                            # not blank and selectbox is picked and
                                                                            # topic_of_interest is not blank then this
                                                                            # is true

    st.write("Hi {0}, you selected the {1} topic.".format(name,             # Will display the user's name and also the
                                                    topic_of_interest))     # the topic they chose in the selectbox

    st.subheader("II - Frequency Distribution")                             # Displays a subheader

    frequency_distribution = st.checkbox("Click here to generate "          # Assigns frequency_distribution with a
                                         "frequency distribution")          # checkbox value

    if frequency_distribution:                                              # If frequency_distribution is checked then
                                                                            # this statement is true

        url = "https://api.nytimes.com/svc/topstories/v2/{}.json?api-key=".format(topic_of_interest) + api_key

                                                                            # Assigns url with the topic url that the
                                                                            # the user is interested in along with my
                                                                            # api key

        response = requests.get(url).json()                                 # Assigns response with the data that url
                                                                            # returns and converts it into a .json file

        main_functions.save_into_file(response, "JSON_File/API_Stories.json")   # Calls save_into_file from
                                                                                # main_functions

        stories = main_functions.read_from_file("JSON_File/API_Stories.json")   # Assigns stories with the value that is
                                                                                # returned when reading API_Stories.json

        abstract = ""

        for i in stories["results"]:                                        # Iterates through the "results" list

            abstract = abstract + i["abstract"]                             # Adds the values inside the "abstract" key
                                                                            # into the abstract variable

        words = word_tokenize(abstract)                                     # Assigns the tokenization of the words in
                                                                            # the variable abstract

        words_wo_punc = []

        for w in words:                                                     # Iterates through all the values in words

            if w.isalpha():                                                 # If words contains letters then this
                                                                            # statement is true

                words_wo_punc.append(w.lower())                             # Adds the values in words into the list
                                                                            # words_no_punc and puts them in lower case

        stopwords = stopwords.words("english")                              # Assigns the list of stop words in english
                                                                            # to stopwords

        clean_words = []

        for w in words_wo_punc:                                             # Iterates through the values in
                                                                            # words_no_punc

            if w not in stopwords:                                          # If words_no_punc does not contain a value
                                                                            # from stopwords then this statement is true

                clean_words.append(w)                                       # Adds the value in words_no_punc into the
                                                                            # the list clean_words

        frqu3 = FreqDist(clean_words)                                       # Assigns frqu3 with the values that show up
                                                                            # frequently in clean_words

        most_common_words = frqu3.most_common(10)                           # Assigns most_common_words with the 10 most
                                                                            # frequent values in frqu3

        words = []

        count = []

        for w in range(10):                                                 # Iterates until it reaches 10

            words.append(most_common_words[w][0])                           # Adds the value of the first index of every
                                                                            # element in most_common_words

            count.append(most_common_words[w][1])                           # Adds the value of the second index of
                                                                            # every element in most_common_words

        y_position = np.arange(len(words))                                  # Assigns y_position with the value of the
                                                                            # space between the values in words based on
                                                                            # the amount of values in words

        plt.figure(figsize=(12, 8))                                         # Creates a figure of 12 by 8 dimensions

        plt.xticks(y_position, words)                                       # Places the values of words based on
                                                                            # y_position

        plt.plot(y_position, count)                                         # Plots the values of count based on
                                                                            # y_position

        plt.xlabel('Words')                                                 # Labels the x-axis 'Words'

        plt.ylabel('Count')                                                 # Labels the y-axis 'Count'

        st.set_option('deprecation.showPyplotGlobalUse', False)             # Removes a warning regarding st.pyplot
                                                                            # having to take arguements

        st.pyplot(plt.show())                                               # Displays the plot graph

    st.subheader("III - Wordcloud")                                         # Displays a subheading

    wordcloud = st.checkbox("Click here to generate wordcloud")             # Assigns wordcloud with a checkbox value

    if wordcloud:                                                           # If wordcloud is checked then this
                                                                            # statement is true

        stories = main_functions.\
            read_from_file("JSON_File/API_Stories.json")                    # Assigns stories with value that is
                                                                            # returned from reading the AP_Stories.json
                                                                            # file

        abstract = ""

        for i in stories["results"]:                                        # Iterates through the "results" list

            abstract = abstract + i["abstract"]                             # Adds the values inside the "abstract" key
                                                                            # into the abstract variable

        wordcloud = WordCloud().generate(abstract)                          # Generates a wordcloud based on the values
                                                                            # in abstract and assigns it to wordcloud

        plt.figure(figsize=(12, 12))                                        # Creates a figure of 12 by 12 dimensions

        plt.imshow(wordcloud)                                               # Displays the data in wordcloud as an image

        plt.axis("off")                                                     # Sets the axis properties of the graph off

        st.set_option('deprecation.showPyplotGlobalUse', False)             # Removes a warning regarding st.pyplot
                                                                            # having to take arguements

        st.pyplot(plt.show())                                               # Displays the wordcloud image

        st.write("Wordcloud generated for {} "                              # Displays text informing the user of the
                 "topic.".format(topic_of_interest))                        # wordcloud that was generated based on
                                                                            # their topic selection

st.header("Part B - Most Popular Articles")                                 # Displays a subheading

st.write("Select if you want to see the most shared, emailed, "             # Displays text telling the user what
         "or viewed articles.")                                             # article types they can select from

article_types = st.selectbox("Select your preferred set of articles",       # Assigns article_types with values of the
                               ["", "shared", "emailed", "viewed"])         # select box

period_of_time = st.selectbox("Select the period of time (last days)",      # Assigns period_of_time with the values of
                              ["", "1", "7", "30"])                         # the select box

if article_types and period_of_time and article_types is not "" and \
        period_of_time is not "":                                           # If article_types has a value and it is not
                                                                            # blank and period_of_time has a value and
                                                                            # it is not blank then this statement is
                                                                            # true

    url = "https://api.nytimes.com/svc/mostpopular/v2/{0}/{1}.json" \
          "?api-key=".format(article_types, period_of_time) + api_key       # Assigns url with the article types and the
                                                                            # recent days associated with those articles
                                                                            # and contains my api key

    response2 = requests.get(url).json()                                    # Assigns response2 with the data that url
                                                                            # returns and converts it into a .json file

    main_functions.save_into_file(response2,                                # Calls the method save_to_file and stores
                                  "JSON_File/Popular_Articles.json")        # the data in response2 into the
                                                                            # Popular_Articles.json file

    stories = main_functions.read_from_file\
        ("JSON_File/Popular_Articles.json")                                 # Assigns stories with the value that is
                                                                            # returned when reading Popular_Articles.json

    abstract2 = ""

    for i in stories["results"]:                                            # Iterates through the "results" list

        abstract2 = abstract2 + i["abstract"]                               # Adds the values inside the "abstract" key
                                                                            # into the abstract variable

    wordcloud2 = WordCloud().generate(abstract2)                            # Generates a wordcloud based on the values
                                                                            # in abstract2 and assigns it to wordcloud2

    plt.figure(figsize=(12, 12))                                            # Creates a figure of 12 by 12 dimensions

    plt.imshow(wordcloud2)                                                  # Displays the data in wordcloud2 as an
                                                                            # image

    plt.axis("off")                                                         # Sets the axis properties of the graph off

    st.set_option('deprecation.showPyplotGlobalUse', False)                 # Removes a warning regarding st.pyplot
                                                                            # having to take arguements

    st.pyplot(plt.show())                                                   # Displays the word cloud image
