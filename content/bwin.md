Title: bwin.com odds API
Date: 2016-08-30 16:51
Category: API

_Searching for and finding an API to poll betting odds from bwin.com by a man-in-the-middle on their official app_

I was searching for interesting statistical data the other day and stumbled across online betting. I never really got into gambling at all and was surprised how popular it is. The market is littered with more or less shady offers. Anyhow none of these seems to be pretty chatty about their data or even has an official API. Therefore I tried to analyze several websites just to find most of those betting providers try to obfuscate their backends API calls as good as they can.
A little disappointed I picked bwin.com (because they offer a hell of a lot of betting data) and started to analyze their mobile application for more insights in how their API works. Using [mitmproxy](https://mitmproxy.org/) I was able to man-in-the-middle the calls to the backend API. There is a good tutorial on how to intercept phone connection with mitmproxy [here](http://www.digitalinternals.com/mobile/android-sniff-http-https-traffic-without-root/490/). It turns out this API is much better to use than the one used by the website.

#Setting up the capture environment
First odd thing I noticed is that the official bwin app is not in Playstore but needs to be downloaded from their site. This leads to a pretty hilarious website and makes bwin assure you about 5 times this app really is legit and you should absolutely install it despite all warnings.

<img src="{filename}/images/bwin4.jpg" alt="Screenshot" style="width: 95%;"/>

So I downloaded the app and set up the capture.  

#First contact
Starting the app caused lot of pollution in mimproxy. From a fresh start I counted 19 connections made to different endpoints. No less than 4 analytics networks are queried by the bwin app: appsflyer.com, eumcollector, mixpanel and google-analytics. Even before I had any interaction with the app my carrier name, device, network type and other things were transferred to third party servers.

Another call caught my attention.
```
GET https://media.itsfogo.com/media/mobile/COM/sports/android/SB_POS3006_config.txt
    ← 200 text/plain 3.6kB 138ms
```
itsfogo.com seems to act as a shared repository for all services offered by the company behind bwin, bwin.party digital entertainment plc in Gibraltar. The certificate has alt names registered for a list of 38! other domains. Most of these domains are clearly related to online gambling and betting like foxybingo.com or partypoker.com. Two domains stick out: intertrader.com claims to be a more serious brooking website and theborgata.com is an actual Casio in Atlantic city (which offers online gambling as well). There is an Outlook mail server hosted at mail.itsfogo.com.

Like the name already suggests `SB\_POS3006_config.txt` is a configuration file for the Android client. The JSON content is very readable. `"application_disabled": false` for example looks like a kill switch for the app and `"application_disabled_comment": "show maintenance message"` explains what happens when its triggered. (Who puts comments in the content of a configuration json file?)  
Things could have ended fast with `"betting_api_url": "",` but its empty. So we get to know that poker is currently not 'cross-sold' to AT, DE and UA and the latest supported app version is 69.  
The next thing of interest is `"legacy_device_url": "https://lite.bwin.com"`. It links to a reduced version of bwin which uses a bit less cluttered API and is also free from a blinking Flash advertisement. If I'd be into online gambling I'd definitely prefer that page over bwin.com. Also we see a long list of which advertisement is currently active in which country like the `Casino slider short appearance promotion`. Last interesting thing is the update .apk URL `http://media.itsfogo.com/media/upload/mobile/android/apk/bwinlive.apk`.

All the analytics and configuration left aside two domains are left.
```
GET https://api.bwin.com/V3/GeoLocation.svc/IP/
   ← 200 application/json 213B 165ms
```
Bwin seems to run their own geolocation API. Because its IP based accuracy is just on a city level in my case. All api.bwin.com calls look very generic and might very well be shared between the website and the mobile app. There is another call to get the current server time and one that contains localized tutorials and names for a lot of sports clubs and countries around the world.

#The actual API
So I had one promising domain left: mobileapi.bwinlabs.com.
```
GET https://en.mobileapi.bwinlabs.com/api/android/v2/events/ms2common?leagueid=43&regionid=17&overview_or_events_switch=...
	← 200 application/json 18.13kB 247ms
```
Good thing is, the response contains betting odds for several soccer related events. Bad thing is all parameters are URL encoded and the response mixes up several tournaments and types of betting. In order to understand the meanings of the request fields I clicked on the 'soccer' category and narrowed my search to only Premier League games. Decoding the URL leads to something better readable.
```
https://en.mobileapi.bwinlabs.com/api/android/v2/events/ms2common?leagueid=46&regionid=14&overview_or_events_switch={events:10,locations:1,leagues:1,keep_overview:true}&sportid=4&markettemplateid=14&overview=&events=&page_size=500&tournamentlist=true&country=uk&ipcountry=uk&partnerid=com.bwinlabs.betdroid_16.7.17&label=com&mediaprovider=unas,perform
```

`/api/android/v2/events/ms2common` is the path for all requests going to the API. Maybe there is another API used for iPhones. I have no clue what ms2common is. 

`sportid=4` clearly marks the sport to search bets for. Basketball is 7, Tennis 5, Ice Hockey 12, Handball 16, Volleyball 18.  
`regionid=14` marks I was searching for soccer in England. RegionIDs are consistent over sports so if Germany is region 17 in soccer it will also be in handball. Of course not every country hosts bets of every sport. `leagueid=46` marks Premier League.  
These three parameters can easily be obtained from [bwin lite](https://lite.bwin.com/en/Sports/Main). Clicking trough the table the URL encodes `https://lite.bwin.com/en/sports/main/regionID/sportID/leagueID`.  
The other parameters control how many and what information are packed into the JSON. So I started stripping the request. `markettemplateid=17` seems to control if only popular offers should be shown or all of them. Removing lead to a 7MB JSON file containing a pretty good list of games and betting odds. With the 'page_size' attribute this huge JSON can be shrinked by only showing the latest n offerings. 
All other request parameters except the `events` keyword can be removed. The original request headers are not needed as well.

#Example
Using that knowledge coding a Python wrapper for basic odd requests is very simple.
```
import requests

def getOdds(regionID, sportID, leagueID, result_size=500):
	parameters ={
		"regionid": regionID,
		"sportid": sportID,
		"leagueid": leagueID,
		"page_size": result_size,
		"events": "",
		"partnerid": "dummy" #Can be anything
	}
	r = requests.get("https://en.mobileapi.bwinlabs.com/api/android/v2/events/ms2common", params=parameters)
	return r.json()

response = getOdds(14, 4, 46, result_size=10) #Query for 10 games

#Working with the response
for game in response["response"]["items"]["events"]: #Iterate over all the games
	odds = game["non_live"]["games"][0]["results"]
	
	name = game["details"]["name"]
	odds1 = str(odds[0]["odds"])
	oddsX = str(odds[1]["odds"])
	odds2 = str(odds[2]["odds"])
	
	print(name.rjust(35), odds1.rjust(5), oddsX.rjust(5), odds2.rjust(5)) #Format the output nicely
```
```
   Manchester Utd - Manchester City  2.35   3.3   2.9
        Bournemouth - West Bromwich   2.0   3.3  3.75
        Arsenal FC - Southampton FC  1.53  4.25   5.5
                Burnley - Hull City   2.2   3.2   3.3
  Middlesbrough FC - Crystal Palace   2.2   3.2   3.3
     Stoke City - Tottenham Hotspur   4.5   3.6  1.75
          West Ham United - Watford  1.85   3.6   4.0
      Liverpool FC - Leicester City  1.62  3.75   5.5
          Swansea City - Chelsea FC   5.5   3.8  1.57
               Sunderland - Everton   3.4   3.3   2.1
```
In general the returned JSON is pretty readable but contains a lot of redundant information.  
Further research could include the mapping from names to IDs and using the API to place an actual bet.

