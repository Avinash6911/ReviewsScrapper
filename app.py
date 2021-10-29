from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

@app.route("/", methods = ["Get"])
def home():
    return render_template('index.html')

@app.route("/extract", methods = ["Post"])
def extract():
    try:
        productName = request.form['content']
        url = "https://www.flipkart.com/search?q=" + productName.replace(" ", "+")
        response = requests.get(url)
        data = bs(response.text, "html.parser")
        contents = data.findAll("div", {"class": "_1AtVbE col-12-12"})
        contents = contents[4:]
        itemLink = "https://www.flipkart.com" + contents[0].div.div.div.a['href']
        response = requests.get(itemLink)
        itemData = bs(response.text, "html.parser")
        reviewDetails = itemData.find_all('div', {'class': '_16PBlm'})
        reviews = []
        for review in reviewDetails:
            try:
                name = review.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text

            except:
                name = 'No Name'

            try:
                rating = review.div.div.div.div.text

            except:
                rating = 'No Rating'

            try:
                heading = review.div.div.div.p.text
            except:
                heading = 'No Comment Heading'
            try:
                comtag = review.div.div.find_all('div', {'class': ''})
                comment = comtag[0].div.text
            except:
                custComment = 'No Customer Comment'
            # fw.write(searchString+","+name.replace(",", ":")+","+rating + "," + commentHead.replace(",", ":") + "," + custComment.replace(",", ":") + "\n")
            mydict = {"Product": productName, "Name": name, "Rating": rating, "Heading": heading,
                      "Comment": comment}  # saving that detail to a dictionary
            # x = table.insert_one(mydict) #insertig the dictionary containing the rview comments to the collection
            reviews.append(mydict)  #
        return render_template('results.html', reviews=reviews)

    except Exception as e:
        print(e)
        return "Something is wrong"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
