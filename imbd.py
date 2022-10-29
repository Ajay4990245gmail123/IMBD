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
            searchString=request.form['movie'].replace(" ","+")
            searchString1 = request.form['movies'].replace(" ", "+")
            SearchMovie=(searchString+":+"+searchString1).title()
            url = "https://www.imdb.com/search/title/?title=+"
            # resp = requests.get(url)
            # print(resp)
            # content = BeautifulSoup(resp.content, 'html.parser')
            Search = url+SearchMovie
            Movie = requests.get(Search)
            one_movie = BeautifulSoup(Movie.text, "html.parser")
            MovieLinkId = one_movie.find_all("h3", class_="lister-item-header")[0].a["href"]
            MainLink = "https://www.imdb.com" + MovieLinkId
            MovieDetail = requests.get(MainLink, "html.parser")
            MovieDetailSoup= BeautifulSoup(MovieDetail.content, "html.parser")
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
            MovieDict={"TypeOfSarch":TypeOfSarch,"MovieName":MovieName,"MovieUrl":MovieUrl ,"HighestRating":HighestRating,"LowRating":LowRating,"avarageRating":ratingValue,"TotalUsers":TotalUsers,"MovieGenr":MovieGenr,"ReleseDate":ReleseDate,"MovieHero":MovieHero,"MovieSupport":MovieSupport,"MovieFemale":MovieFemale,"MovieDirector":MovieDirector,"MovieDuration":MovieDuration}
            MovieInformation.append(MovieDict)
            #return render_template("resultPage.html",revi=MovieInformation[0:1])
            # return(MovieInformation)
            #
            # searchString = request.form['movie'].replace(" ", "+")
            # searchString1 = request.form['movies'].replace(" ", "+")
            # SearchMovie = (searchString + ":+" + searchString1).title()
            # print(SearchMovie)
            # url = "https://www.imdb.com/search/title/?title=+"
            # print(url)
            #        # resp = requests.get(url)
            #        # print(resp)
            #        # content = BeautifulSoup(resp.content, 'html.parser')
            # Search = url + SearchMovie
            # print(Search)
            #        # NewLink =BeautifulSoup(Search, "html.parser")
            #        # print(NewLink)
            # Movie = requests.get(Search)
            # print(Movie)
            # one_movie = BeautifulSoup(Movie.text, "html.parser")
            #        # print(one_movie)
            # MovieLinkId = one_movie.find_all("h3", class_="lister-item-header")[0].a["href"]
            # MainLink = "https://www.imdb.com" + MovieLinkId
            # print(MainLink)
            #        # ActiveLink = BeautifulSoup(MainLink, "html.parser")
            # MovieDetail = requests.get(MainLink, "html.parser")
            # MovieDetailSoup = BeautifulSoup(MovieDetail.content, "html.parser")

            review_link1 = MovieDetailSoup.find_all("a",class_="ipc-link ipc-link--baseAlt ipc-link--touch-target sc-124be030-2 eshTwQ isReview")[0]["href"]
            Review_detail = 'https://www.imdb.com' + review_link1
            active_link_2 = BeautifulSoup(Review_detail, "html.parser")
            review_scrap = requests.get(active_link_2)
            review_scrap_details = BeautifulSoup(review_scrap.text, "html.parser")
            review_1 = review_scrap_details.find_all("div", class_="review-container")
            MovieReviwes=[]
            for Review in review_1:
                try:
                    name=Review.div.find_all("span",class_="display-name-link")[0].text
                except:
                    name=" name is not available in this page"
                try:
                    MovieRating=Review.div.find_all("span",class_="")[0].text
                except:
                        MovieRating= " movie rating is not available in this movie"
                try:
                    HeadComment=Review.div.find_all("a",class_="title")[0].text
                except:
                    HeadComment=" header comment not available in this page"
                try:
                    Comment=Review.find_all("div", class_="text show-more__control")[0].text
                except:
                    Comment= " comments is not available in this  movie"
                try:
                    ReviewDate=Review.div.find_all("span",class_="review-date")[0].text
                except:
                    ReviewDate= " review date not availablee"

                ReviewDict={ "name":name,"MovieRating":MovieRating,"HeadComment":HeadComment,"Comment":Comment,"ReviewDate":ReviewDate}
                MovieReviwes.append(ReviewDict)

            return render_template("resultPage.html",reviwes=MovieReviwes[0:len(MovieReviwes)])
        except:
            return " pls check once movie name"

if __name__=="__main__":

   app.run(debug=True)