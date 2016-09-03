Title: Manipulating 'Langenscheid Jugendwort des Jahres'
Date: 2016-09-30 23:50
Category: API

_Manipulating the election of the German youth word of the year_

#Setup
The German Publisher Langenscheid once a year holds a poll for the 'youth word of the year'. Like every time this year 30 more or less hilarious words can be voted for by the beloved social media community. Most of them are totally unknown to me. But I like one word to win: 'Tintling'.

So a friend and me backtracked the voting request.

<img src="{filename}/images/juwo1.png" alt="Screenshot" style="width: 95%;"/>

It was not even HTTPS. The only protection we found against flooding was the super slow server. Just resending the request gave a nice and clean HTTP 200 response. But could this have been all? Maybe there was some more sophisticated protection in the background?

#Execution
So we wrote a script that shuffels the Cookie parameters a bit and changed the User-Agent to a good looking Windows NT one. Because the server was so slow 20 requests are send in parallel to make the voting a bit faster. We will publish the code as soon as this is fixed by Langenscheidt.

To proove our script works we took another entry which was not already #1 and started the voting. Here is a screenshot of 'Googleschreiber' before we started.

<img src="{filename}/images/juwo2.png" alt="Screenshot" style="width: 80%;"/>

And here is one after:

<img src="{filename}/images/juwo3.png" alt="Screenshot" style="width: 80%;"/>

We were able to increase the position by 0.1% using 2000 requests. A lot of these requests returned "0" instead of "1" so they probably did not count. Also a few of the requests did return HTTP 500 answers. But still: Langenscheid ain't the best when it comes to securing their poll. Using more threads the website got even slower than it already was, so we refrained from that. Also the results page did not load anymore. We did not want to DDOS anything but just show how easy the manipulation is. 
