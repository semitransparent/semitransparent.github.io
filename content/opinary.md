Title: Manipulate Opinary polls
Date: 2016-09-02 17:33
Category: Polls

_Manipulating the results of a popular poll service_

Reading some [news pages](http://www.welt.de/politik/deutschland/article157917484/Warum-Fluechtlinge-Mecklenburg-Vorpommern-lieben.html) I came accross a new type of online polls. Instead of asking questions the poll allows me to move the needle of a compass and then gives a graphical feedback on how other users voted. 
<img src="{filename}/images/opinary2.png" alt="Screenshot" style="width: 40%;"/>

These polls reminded me of old online polls that could easily be manipulated by refreshing the page and voting for the same thing over and over again. But the [Opinary](http://opinary.com/) poll seemed more clever. Refreshing the page led to nothing but the result I already voted for. Even after clearing the cookies my result stayed the same. In Incognito mode I was able to vote multiple times but that did not seem like a very scalable approach. The little counter told me 15.000 users had already voted and every time I refreshed the page some very annoying autoplay video started. Also it took ages to reload all the advertisements.  

To find a bit way I fired up mitmproxy once more and found the request done to create a new vote.
<img src="{filename}/images/opinary3.png" alt="mitmproxy screenshot" style="width: 80%;"/>

First odd thing I noticed: The request is not even https so Wireshark would have been enough. Its a simple post to some remote URL and does not contain much data. `x` and `y` are obiously I choose on the location in the compass, there is an id in there and a field alled `comment_auth`. Simply resending the request did not work, the counter on the website did not increase. So I started playing with the `comment_auth` token but the counter still stayed the same. Therefore some more sphisticated function had to be in place in that generates *valid* tokens for the API. In order to find it I went into the glorious Chrome debugger and deobfuscated the Code. By setting a breakpoint I was able find the function call that generates the `comment_auth` token. Lukily the .coffee source files of the complete plugin where delivered with the compiled .js so I did not have to deal with the obfuscated JavaScript for long. This is perfect for debugging but why would you do this in a production instance?  
Digging my way trough the function calls I ended up at a promising file. 

```
// via: http://stackoverflow.com/a/2117523/2511985

function getUniqueId(){
  var str = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx';
  return str.replace(/[xy]/g, function(c) {
    var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
    return v.toString(16);
  });
}
```
Props for naming the stackoverflow thread the code orginates from, but its just some generic GUID generation. I triple checked the call stack but that was definitly the generator for the `comment_auth` field in the request. So why did my manual manipulation of the GUID did not work? Maybe the number of users that voted was not updated in realtime?

To find that out I wrote a small script that constructs a vote request every second. Then I measured how many votes are created by real users during a 8 minute timeframe. After that I fired up my script and measured for 8 more minutes. The results met my expectations. I was able to take control of the needle and vote 8x more than all other voters in that timeframe combined.
<img src="{filename}/images/opinary5.png" alt="graph of vote results" style="width: 80%;"/>

Using this glitch opinary polls can easily be manipulated to show the desired result. Opinary is used by several German news sites like Spiegel Online, welt.de and the Huffington Post. I tried to get in touch with Opinary but there has not been any reaction to my mails.
<img src="{filename}/images/opinary4.png" alt="manipulated result" style="width: 40%;"/>

