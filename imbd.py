from flask import Flask,render_template,request
from bs4 import BeautifulSoup
from flask_cors import CORS,cross_origin
import requests
import json
app=Flask(__name__)
@app.route("/",methods=["GET"])
@cross_origin()
def tag_1():
    return render_template("index2.html")
@app.route('/reviews',methods=["GET","POST"])
@cross_origin()
def new_line():
    if request.method=="POST":
        try:

            searchString = request.form['movie'].replace(" ", "+") # user search
            searchString1 = request.form['movies'].replace(" ", "+")
            SearchMovie = (searchString + ":+" + searchString1).title() #concat searchString and searchString1
            url = "https://www.imdb.com/search/title/?title=+"
            Search = url + SearchMovie      #concate two links
            Movie = requests.get(Search) #get link html response
            one_movie = BeautifulSoup(Movie.text, "html.parser") # beatified the html content
            MovieLinkId = one_movie.find_all("h3", class_="lister-item-header")[0].a["href"]
            MainLink = "https://www.imdb.com" + MovieLinkId #concate main link to movie link
            print(MainLink)
            MovieDetail = requests.get(MainLink, "html.parser") #get one movie link response
            MovieDetailSoup = BeautifulSoup(MovieDetail.content, "html.parser") # beatified the one movie  html content
            #get reviews link
            review_link1 = MovieDetailSoup.find_all("a",class_="ipc-link ipc-link--baseAlt ipc-link--touch-target sc-124be030-2 eshTwQ isReview")[0]["href"]
            Review_detail = 'https://www.imdb.com' + review_link1  # concate main link to reviews link

            review_scrap = requests.get(Review_detail) # checking  response
            review_scrap_details = BeautifulSoup(review_scrap.text, "html.parser")# beatified reviews  html content
            review_1 = review_scrap_details.find_all("div", class_="review-container") # getting all reviews of one movie
            MovieReviwes=[]   #create empty list
            for Review in review_1: # using for loop
               # using try and except
                try:
                    # getting movie name
                    name=Review.div.find_all("span",class_="display-name-link")[0].text
                except:
                    name=" name is not available in this page"
                try:
                    #getting movie rating
                    MovieRating=Review.div.find_all("span",class_="")[0].text
                except:
                        MovieRating= " movie rating is not available in this movie"
                try:
                     #getting header comment
                    HeadComment=Review.div.find_all("a",class_="title")[0].text
                except:
                    HeadComment=" header comment not available in this page"
                try:
                    #getting main comment
                    Comment=Review.find_all("div", class_="text show-more__control")[0].text
                except:
                    Comment= " comments is not available in this  movie"
                try:
                    #get review posting date
                    ReviewDate=Review.div.find_all("span",class_="review-date")[0].text
                except:
                    ReviewDate= " review date not availablee"
                # all information save in dictionary format key:value
                ReviewDict={ "name":name,"MovieRating":MovieRating,"HeadComment":HeadComment,"Comment":Comment,"ReviewDate":ReviewDate}
                #append information  ReviewDict to  movie reviews
                MovieReviwes.append(ReviewDict)
                #using flask templates
            return render_template("resultPage.html",reviwes=MovieReviwes[0:len(MovieReviwes)])
        except:
            return " pls check once movie name"

if __name__=="__main__":

   app.run(debug=True)