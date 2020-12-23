from flask import Flask, render_template,redirect,url_for
from flask_ask import Ask, statement, question
import datetime
import logging
from flask_mysqldb import MySQL
import random
import requests, json
import unicodedata
import cgitb
import urllib.request
import webbrowser
cgitb.enable()
import emoji

app = Flask(__name__)
ask = Ask(app, '/')


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'karan1696'
app.config['MYSQL_DB'] = 'myalexa'

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

mysql = MySQL(app)


api_key = "c9a0d14cd73a71d381378454be7a9ba2"
base_url = "http://api.openweathermap.org/data/2.5/weather?&units=metric&"






global s


try:
    @ask.launch
    def start_skill():
         display = render_template('welcome')
                return question(display)
     

    @ask.intent('NameIntent')
    def p_name(f_name):
        display = render_template('name', f_name=f_name)
        return question(display)

    @ask.intent('locationIntent')
    def location():
        display="tell me your location"
        return question(display)


    @ask.intent('NewsIntent')
    def news():
        display = webbrowser.open("https://timesofindia.indiatimes.com/news")
        print(display)
        return question('anything else you want')


    @ask.intent('SearchIntent')
    def search(things):
        display=webbrowser.open("https://en.wikipedia.org/wiki/"+things+"")
        print(display)
        global s
        s=things
        return redirect(url_for(query,s=s))
       

    @ask.intent('QueryIntent')
    def query(req):
        return question(req)


    @ask.intent('WeatherIntent')
    def p_age(city):
        complete_url = base_url + "appid=" + api_key + "&q=" + city
        response = requests.get(complete_url)
        x = response.json()
        # print(x)
        t = float(x['main']['temp'])
        temp=str(t)
        ans=" current temperature in "+city+" is "+temp+"  "
        return question(ans)


    @ask.intent('AskIntent')
    def f_ask():
        display = render_template('ask')
        return question(display)

    @ask.intent('CurrentIntent')
    def f_current():
        c = datetime.datetime.now()
        s=c.strftime("%a, %b %d, %Y")
        display="today is "+s+" , anything else you want"
        return question(display)

    @ask.intent('TimeIntent')
    def f_time():
        c = datetime.datetime.now()
        s=c.strftime("%I:%M %p")
        display=""+s+" , anything else you want"
        return question(display)

    @ask.intent('AMAZON.FallbackIntent')
    def f_error():
        display="I cannot understand what you say , please say it again"
        return question(display)

    @ask.intent('ByeIntent')
    def bye():
        display = render_template('byee')
        return statement(display)


    @ask.intent('JokeIntent')
    def joke():
        cur = mysql.connection.cursor()
        n=random.randint(1,3)
        n=str(n)
        cur.execute("select joke from alexa where id = '"+n+"'")
        data = cur.fetchone()
        mysql.connection.commit()
        cur.close()
        sql = ''.join(data)
        return question(sql)
    
except:
    d="Their is something wrong in your input, please ask something else"
    print(d)

if __name__ == '__main__':
    app.run(debug=True)


