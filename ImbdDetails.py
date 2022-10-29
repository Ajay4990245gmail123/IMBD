from flask import Flask,render_template,request
from bs4 import BeautifulSoup
from urllib.request import urlopen as uropen
import requests
import json
app=Flask(__name__)
@app.route("/",methods=["GET"])
def tag_1():
    return render_template("index2.html")
@app.route('/reviews',methods=["GET","POST"])
def new_line():
    if request.method=="POST":
        try:
            searchString=request.form['movie'].replace(" ","+")
            searchString1 = request.form['movies'].replace(" ", "+")
            SearchMovie=(searchString+":+"+searchString1).title()
            url = "https://www.imdb.com/search/title/?title=+"
            Search = url+SearchMovie
            Movie = requests.get(Search)
            one_movie = BeautifulSoup(Movie.text, "html.parser")
            MovieLinkId = one_movie.find_all("h3", class_="lister-item-header")[0].a["href"]
            MainLink = "https://www.imdb.com" + MovieLinkId
            MovieDetail = requests.get(MainLink, "html.parser")
            MovieDetailSoup = BeautifulSoup(MovieDetail.content, "html.parser")
            MovieDetailFind = MovieDetailSoup.find_all("script")
            type_of=MovieDetailFind[2].text
            MovieData=json.loads(type_of)
            TypeOfSarch=MovieData["@type"]
            MovieName=MovieData["name"]
            MovieUrl = MovieData["url"]
            HighestRating=MovieData["review"]["reviewRating"]["bestRating"]
            LowRating=MovieData["review"]["reviewRating"]["worstRating"]
            ratingValue=MovieData["review"]["reviewRating"]["ratingValue"]
            TotalUsers=MovieData["aggregateRating"]["ratingCount"]
            MovieGenr=MovieData["genre"]
            ReleseDate=MovieData["datePublished"]
            MovieHero=MovieData["actor"][0]["name"]
            MovieSupport=MovieData["actor"][1]["name"]
            MovieFemale = MovieData["actor"][2]["name"]
            MovieDirector=MovieData["director"][0][ 'name']
            MovieDuration=MovieData["duration"]
            MovieInformation=[]
            MovieDict={"TypeOfSarch":TypeOfSarch,"MovieName":MovieName,"MovieUrl":MovieUrl ,"HighestRating":HighestRating,"LowRating":LowRating,"avarageRating":ratingValue,"TotalUsers":TotalUsers,"MovieGenr":MovieGenr,"ReleseDate":ReleseDate,"MovieHero":MovieHero,"MovieSupport":MovieSupport,"MovieFemale":MovieFemale,"MovieDirector":MovieDirector,"MovieDuration":MovieDuration                }
            MovieInformation.append(MovieDict)
            return render_template("results.html" ,reviews=MovieInformation[0:len(MovieInformation)])

        except:
            return "Movie details not available in this page"

if __name__=="__main__":
   app.run( debug=True)