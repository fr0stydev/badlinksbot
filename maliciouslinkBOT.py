import socket, string, re, requests, json
import pandas as pd
import numpy as np
import random

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
 
# Set all the variables necessary to connect to Twitch IRC
HOST = "irc.twitch.tv"
NICK = "****" #your twitch bot name
PORT = 6667
PASS = "*******" #your twitch oauth code here!
readbuffer = ""
MODT = False
 

# Connecting to Twitch IRC by passing credentials and joining a certain channel
s = socket.socket()
s.connect((HOST, PORT))
s.send(str.encode("PASS " + PASS + "\r\n"))
s.send(str.encode("NICK " + NICK + "\r\n"))
s.send(str.encode("JOIN #(****) \r\n")) #your channel name

urls_data = pd.read_csv("data.csv", encoding = "utf-8")
urls_data.head()

IRC_RE = re.compile(r"(:(?P<nick>[^ !@]+)(\!(?P<user>[^ @]+))?(\@(?P<host>[^ ]+))? )?(?P<command>[^ ]+) (?P<params1>([^:]*))(?P<params2>(:.*)?)")
URL_RE = re.compile(r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*", re.MULTILINE|re.UNICODE)

# Method for sending a message

def send_message(message):
    s.send(str.encode("PRIVMSG #thefrosty0806 :" + message + "\r\n"))

send_message("The BOT is now connected, please type in !bot")


def translate(m):
  m = IRC_RE.match(m.strip())
  if not m:
    return None
  m = m.groupdict()
  m["params"] = m.pop("params1").split()
  if m["params2"]:    m["params"] += [m["params2"][1:]]
  m.pop("params2")
  return m
#Making Tokens
def makeTokens(f):
    tkns_BySlash = str(f.encode('utf-8')).split('/')
    total_Tokens = []
    for i in tkns_BySlash:
        tokens = str(i).split('-')	
        tkns_ByDot = []
        for j in range(0,len(tokens)):
            temp_Tokens = str(tokens[j]).split('.')
            tkns_ByDot = tkns_ByDot + temp_Tokens
        total_Tokens = total_Tokens + tokens + tkns_ByDot
    total_Tokens = list(set(total_Tokens))	
    if 'com' in total_Tokens:
      total_Tokens.remove('com')	
    if 'www' in total_Tokens:
      total_Tokens.remove('www')
    return total_Tokens
y = urls_data["label"]
url_list = urls_data["url"]
vectorizer = TfidfVectorizer(tokenizer=makeTokens)

X = vectorizer.fit_transform(url_list)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.6, random_state=42)

logit = LogisticRegression()
logit.fit(X_train, y_train)

print ("Accuracy ",logit.score(X_test, y_test))

fd = s.makefile()
while True:
  line = fd.readline().rstrip("\r\n")
  commands = translate(line)
  print(commands)

  if commands['command'] == 'PRIVMSG':
    user = commands['user']
    msg = commands['params'][1]
    url = URL_RE.match(msg) 
    if url: 
      print(user)
      print(msg)
      X_predict = [] 
      X_predict.append(msg) 
      print X_predict
      X_predict = vectorizer.transform(X_predict)
      New_predict = logit.predict(X_predict)
      print (New_predict)
      if New_predict == "bad":
        send_message('/timeout ' + user + " 1")
        send_message('That link is malicious! ' + user)
      if New_predict == "good":
        send_message('That link is clean! ' + user)
    else:
      print(user)
      print(msg)
      if msg == "!bot":
        send_message('This is a malicious link detector for my Cyber Security Seminar!')
      elif msg == "Hi":
        send_message("We were expecting you " + user + ".")
      else:
        send_message("Try typing !bot or Hi into the IRC")
  elif commands['command'] == 'PING':
    s.send("PONG tmi.twitch.tv\r\n")