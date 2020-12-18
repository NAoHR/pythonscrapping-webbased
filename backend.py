from flask import Flask,render_template,request,url_for,redirect,session
from bs4 import BeautifulSoup
import datetime
import requests
import os

app = Flask(__name__)
app.secret_key = "akwokodqojdqowmeoqmweoqmeoqjodqwrohgq123123%^#^@&@%T$"
song = []

@app.route("/lryscrap",methods=["POST","GET"])
def home():
	if request.method == "POST":
		global lagu2
		session["pilih"] = request.form['song']
		lagu2 = "".join(map(str,(request.form["song"])))
		plus = lagu2.replace(" ","+")
		try:
			page = requests.get('https://search.azlyrics.com/search.php?q='+plus)
			soup = BeautifulSoup(page.content,"html.parser")
		except requests.exceptions.ConnectionError:
			return "no Connection"
		pemisahan = soup.find(class_='table table-condensed')
		try:
			global link
			link = pemisahan.find_all('td',class_='text-left visitedlyr')
		except AttributeError:
			return render_template("errorhandling.html",errormessage="try another song")
		global kumpulan
		kumpulan = []
		j = 0
		for item in link:
			j +=1
			if j <= 6:
				kumpulan.append(item)
		return redirect(url_for("pilih"))
	return render_template("newindex.html")
@app.route("/lagu",methods=["POST","GET"])
def pilih():
	lagu = "".join(map(str,song))
	if request.method == "POST":
		try:
			number = int(request.form["pilihan"])
		except ValueError:
			errormessage = "u choose nothing"
			return render_template("errorhandling.html",errormessage=errormessage)
		try:
			seperate = kumpulan[number-1]
		except IndexError:
			return render_template("errorhandling.html",errormessage="You choose nothing")
		seperate1 = [item for item in seperate]
		close = str(seperate1)
		go_to = close[close.find('//')+2:close.find('>')-1]
		final = "https://"+go_to
		page = requests.get(final)
		soup = BeautifulSoup(page.content,"html.parser")
		lyrics = soup.find('div',attrs={"class":None,"id":None})
		try:
			global final1
			final1 = str(lyrics)
			final3 = final1.strip("<br>")
			final4 = final3.strip("<br/>")
			final6 = final4.strip("div> <!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->")
			final8 = final6.replace("<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->","")
			final7 = final8.strip("</div")
			final9 = final7.replace("<i>","")
			final10 = final9.replace("</i>","")
			global final5
			final5 = "".join(map(str,final10))
			return render_template("hasil_akhir.html",r=final5)
		except AttributeError:
			return render_template("errorhandling.html",errormessage="ERROR")
	if "pilih" in session:
		try:
			return render_template("choose.html",test=link)
		except NameError:
			return redirect(url_for("home"))
	else:
		return redirect(url_for("home"))
@app.route("/result")
def finale():
	return render_template("hasil_akhir.html",r=final5)
# @app.route("/test",methods=['POST','GET'])
# def anjay():
# 	return render_template('test.html')
# @app.route("/work",methods=['POST','GET'])
# def mantap():
# 	return render_template('newindex.html')
# @app.route("/lryscrap/lagu")
# def pilih():
# 	return song

