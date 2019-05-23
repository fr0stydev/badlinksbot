# BadLinks
A simple Twitch Malicious URL Detector BOT written in Python
Detects bad links

## Purpose
To help streamer filter out the bad URLs by automatically deleting them in their IRC

## Machine Learning

Uses the standardized machine learning module to detect benign/malicious URLs


## Easy to Implement!

All your files are listed in the file explorer. You can switch from one to another by clicking a file in the list.

#### Set all the variables necessary to connect to Twitch IRC

HOST =  "irc.twitch.tv"

NICK =  "****"  #your twitch bot name

PORT =  6667

PASS =  "*******"  #your twitch oauth code here!

s.send(str.encode("JOIN #(****) \r\n")) #your channel name

