Title: Manipulating 'Langenscheid Jugendwort des Jahres'
Date: 2016-09-02 23:50
Category: Polls

_Manipulating the election of the German youth word of the year_

The German Publisher Langenscheid once a year holds a poll for the 'youth word of the year'. Like every time this year 30 more or less hilarious words can be voted for by the beloved social media community. Most of them are totally unknown to me. But I like one word to win: 'Tintling'.

So a friend and me backtracked the voting request.

<img src="{filename}/images/juwo1.png" alt="mitmproxy voting request" style="width: 95%;"/>

It was not even HTTPS. The only protection we found against flooding was the super slow server. Just resending the request gave a nice and clean HTTP 200 response. But could this have been all? Maybe there was some more sophisticated protection in the background?

#Execution
So we wrote a script that shuffels the Cookie parameters a bit and changed the User-Agent to a good looking Windows NT one. Because the server is so slow multiple requests are send in parallel to make the voting a bit faster. We will publish the code as soon as this is fixed by Langenscheidt.
To prove our script works we took another entry which was not already #1 and started the voting. Here is a screenshot of "Googleschreiber" before we started.

<img src="{filename}/images/juwo2.png" alt="Poll before" style="width: 80%;"/>

And here is one after a few minutes.

<img src="{filename}/images/juwo3.png" alt="Poll after" style="width: 80%;"/>

We were able to increase the position by 0.1% using 2000 requests. A lot of these requests returned "0" instead of "1" so they probably did not count. Also a few of the requests did return HTTP 500 answers. In total about 100 requests were delivered to the server and returned "1". Therefore Langescheidt seems to have about 100.000 votes collected already. 
Now we were eager to boost "Googleschreiber's" counter a bit more. But using more threads the website got even slower than it already was, so we refrained from that. Also the results page did not load anymore as soon as one of us used more than than one or two requests per second. Because we did not want to DDOS anything but just show how easy the manipulation is "Googleschreiber" is still on a miserable position.

Using Twitter we tried to get in touch with Langescheidt but they did not react in any way.

**Update 09/09/2016**

The result page is now completely broken, all percentages went mad.
<img src="{filename}/images/juwo4.png" alt="Poll after" style="width: 70%;"/>


