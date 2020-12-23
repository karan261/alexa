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
#from playsound

# from ask_sdk_core.handler_input import HandlerInput
# from ask_sdk_core.dispatch_components import AbstractRequestHandler
# from ask_sdk_core.utils import is_request_type
# from ask_sdk_model.ui import SimpleCard
# from ask_sdk_model import Response

app = Flask(__name__)
ask = Ask(app, '/')


# def googlelink():
#      return ('<div><a href="%s">%s</a></div>' % ("https://www.google.com","Google"))

#
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'karan1696'
app.config['MYSQL_DB'] = 'myalexa'
#
logging.getLogger("flask_ask").setLevel(logging.DEBUG)
# # Set the skill id
#
mysql = MySQL(app)


api_key = "c9a0d14cd73a71d381378454be7a9ba2"
base_url = "http://api.openweathermap.org/data/2.5/weather?&units=metric&"
# Convert the HTTP request headers and body into native format
# of dict and str respectively, and call the dispatch method.

# Convert the response str into web service format and return.






global s


try:
    @ask.launch
    def start_skill():

        # msg = """
        #    <html>
        #    <body>
        #    <button>hello world</button>
        #    </body>
        #    </html>"""

        # btnArray = []
        # btnArray.append(
        #      {"content_type": "text", "title": "Activate UAN password"})
        #
         display = render_template('welcome')
       # display='<div><a href="%s">%s</a></div>' % ("https://www.google.com","Google")
    #welcome_message = 'hello , happy to see you, please tell me your first'
        # display=render_template('myhtml')
        # display =emoji.emojize(":grinning_face:")
        #return question('ok')

        # display = webbrowser.open("https://www.google.com")
        # print(display)
         return question(display)
        # return render_template('myhtml')

    @ask.intent('NameIntent')
    def p_name(f_name):
        display = render_template('name', f_name=f_name)
        return question(display)

    # @ask.intent('AgeIntent')
    # def p_age(f_age):
    #     display = render_template('age', f_age=f_age)
    #     return question(display)
    #
    # @ask.intent('MobileIntent')
    # def p_mob(f_mob):
    #     display = render_template('mobile',f_mob=f_mob)
    #     return question(display)

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
        # return question('okkkk')

    @ask.intent('QueryIntent')
    def query(req):
        return question(req)

        # print(s)
        # s="hello"
        # return question(req)

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
        #print(n)
        cur.execute("select joke from alexa where id = '"+n+"'")
        data = cur.fetchone()
        mysql.connection.commit()
        cur.close()
        sql = ''.join(data)
        return question(sql)
    # @ask.intent('MoodIntent')
    # def mood():
    #     display="tell me your mood"
    #     return question(display)

    # @ask.intent('FlirtIntent')
    # def flirt():
    #     cur = mysql.connection.cursor()
    #     n = random.randint(1, 3)
    #     n = str(n)
    #     #print(n)
    #     cur.execute("select flirt from alexa where id = '" + n + "'")
    #     data = cur.fetchone()
    #     mysql.connection.commit()
    #     cur.close()
    #     sql = ''.join(data)
    #     return question(sql)
    #




except:
    d="Their is something wrong in your input, please ask something else"
    print(d)

if __name__ == '__main__':
    app.run(debug=True)


