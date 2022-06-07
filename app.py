# for more information - https://jinja.palletsprojects.com/en/2.11.x/templates/#base-template

from flask import Flask, render_template, escape, request, json, jsonify, make_response, redirect, url_for, render_template, session, flash
from flask import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from xml.dom import minidom
from datetime import datetime
import requests
from threading import Timer
from flask import request
import time
from itertools import zip_longest
from datetime import datetime
import sqlite3
import os
import os.path
import random
import urllib.request
from urllib.parse import urlparse,urljoin
from bs4 import BeautifulSoup
import requests,uuid,pathlib,os
from fake_useragent import UserAgent
ua = UserAgent()




app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vrkarqgzzzkmtn:0e32017efa344188261e0ca0fa2fe78a0c7f986a6604ce207a4921ca072f4b4e@ec2-34-246-155-237.eu-west-1.compute.amazonaws.com:5432/de51kvccijsfj2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Creating model table for our CRUD database
class Channels(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    channel_name = db.Column(db.String(100))
    channel_logo = db.Column(db.String(100))
    channel_src = db.Column(db.String(100))


    def __init__(self, id, channel_name, channel_logo, channel_src):

        self.id = id
        self.channel_name = channel_name
        self.channel_logo = channel_logo
        self.channel_src = channel_src





#Creating model table for Series
class Series(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    series_name = db.Column(db.String(100))
    series_logo = db.Column(db.String(100))
    series_src = db.Column(db.String(100))


    def __init__(self, series_name, series_logo, series_src):

        self.series_name = series_name
        self.series_logo = series_logo
        self.series_src = series_src


#Creating model table for Series
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    movies_name = db.Column(db.String(100))
    movies_logo = db.Column(db.String(100))
    movies_src = db.Column(db.String(100))


    def __init__(self, movies_name, movies_logo, movies_src):

        self.movies_name = movies_name
        self.movies_logo = movies_logo
        self.movies_src = movies_src


# #Creating model table for our CRUD database
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    registration_date = db.Column(db.DateTime(100))

    def __init__(self, firstname, lastname, email,username, password, registration_date):

        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.password = password
        self.registration_date = registration_date


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    comment = db.Column(db.String(100))
    comment_date = db.Column(db.DateTime(100))

    def __init__(self, username, comment, comment_date):

        self.username = username
        self.comment = comment
        self.comment_date = comment_date


mytree=minidom.parse("static/guide.xml")

full_date = datetime.date(datetime.now())
today = full_date.strftime("%Y%m%d")

current = datetime.now() # current date and time

now = current.strftime("%H%M%S")


@app.route('/')
def index():

    return render_template("home.html")




@app.route('/tv', methods = ['POST', 'GET'])
def tv():


    posters = []

    cwd = os.getcwd()
    pic_path = cwd+"/static/images/posters"

    files = os.listdir(pic_path)
    for file in files:

        file = file[:-4]


        posters.append(file)

    i = 0
    index = 0
    programs = []
    total_len = len(Channels.query.all())
    epg = [[] for x in range(0,total_len)]

    programme = mytree.getElementsByTagName("programme")
    for channel in Channels.query:

        for program in programme:



            start_time = program.getAttribute("start")[8:15]
            finish_time = program.getAttribute("stop")[8:15]
            index += 1

            if channel.channel_name == program.getAttribute("channel"):

                epg[i].append({'start_time':start_time,'finish_time':finish_time,'program':program.childNodes[1].childNodes[0].data})


                if program.childNodes[1].childNodes[0].data not in programs:

                    programs.append(program.childNodes[1].childNodes[0].data)

            index = 0

        i += 1

    x = 0
    channels_lst = []
    for channel in Channels.query:

       channels_lst.append(
           {
           'channel_name': channel.channel_name,
           'channel_logo': channel.channel_logo,
           'src': channel.channel_src,
           'epg':epg[x]

           },)

       x += 1

    return render_template("tv.html", channels=channels_lst, programs=programs)














@app.route('/save_posters', methods = ['POST', 'GET'])
def save_posters():

    if request.method == 'POST':
        img = request.form['img']
        title = request.form['title']

        print("save posters function")
        print(f"img {img} title {title} ")


        import os
        cwd = os.getcwd()



        pic_path = cwd+"/static/images/posters"


        print(pic_path)

        new_path = "D:\\Storage\\Documents\\Python\\Flask\\TVSITE\\Project22\\static\\images\\posters"


        r = requests.get(img)




        # wb means write bytes
        with open(pic_path+"/"+title+".jpg", "wb") as pic:
            pic.write(r.content)


    return jsonify("img")




@app.route('/scrape_for_posters', methods = ['POST', 'GET'])
def scrape_for_posters():



    print("scrape for posters")

    if request.method == 'POST':


        try:
            global requested_url,specific_element,tag

            title = request.form['q']


            print(title)


            site = "https://kinokrad.co?do=search&subaction=search&story="
            site = site+title

            headers = {"User-Agent" : ua.random}

            response = requests.get(site, headers=headers)


            soup = BeautifulSoup(response.text, 'lxml')



            search_item = soup.find_all("div", class_="searchitem")

            print(len(search_item))

            print(search_item[0])

            data = []
            for s_item in search_item:


                img_path = "https://kinokrad.co"+s_item.find("div", class_="postershort").find("img").get("src")


                data.append(
                {
                    'title' : title,
                    'img': img_path,
                    'href': s_item.find("div", class_="postershort").find("a").get("href"),


                },)

            print(data)



            href = search_item.find("div", class_="postershort").find("a").get("href")
            img = search_item.find("div", class_="postershort").find("img").get("src")








        except Exception as e:
            flash("Image hasnt been found on site", "danger")




    return jsonify(data)












if __name__ == '__main__':

    app.run()

