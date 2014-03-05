pySpidy 
=======
*A simple, yet powerful, Python web crawler for Google with browser capabilities*

pySpidy is a Python (2.7) webcrawler for Google with browser capabilities. It does Google queries and mine the data from the resulting webpages, including title, link, date and description. It saves everything to a CSV file.

Intro
-----

pySpidy was born out of a mid-2013 personal project to extract information from Google and export it to a CSV file. I'm a journalist who happens to code a little in Python. At that time, I couldn't find any Python crawlers that worked with Google. They were either broken or Google had banned them. It may be the case that Google has already banned mine. They are very good at figuring out your robot is not a person using an actual browser.

Bear in mind that Google doesn't approve scraping their search results. For that, they have a [custom search API](https://developers.google.com/custom-search/json-api/v1/overview). For free, you get 100 results per day. More than that you'll have to show them your monies. Use this tool at your own discretion.

How does it work?
-----------------

Internally, pySpidy works by defining a class which holds all the information of the query, such as link, date, description and title. There is a browser object (powered by [mechanize](http://wwwsearch.sourceforge.net/mechanize/)) that handles the HTTP requests. Those are parsed to a [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/) object that are manipulated by data-mining helper funcions. The crawler itself is a simple script that calls those functions and cycle through the result pages at Google. It stores everything it finds in a CSV file. It tells you mostly everything it does in the console and it handles some errors with more than just a callback.

pySpidy uses two external Python libraries:

  * [mechanize](http://wwwsearch.sourceforge.net/mechanize/) - Stateful programmatic web browsing in Python 
  * [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/) - allows you to scrape the HTML documents easily

...and some built-in stuff:

  * [csv](http://docs.python.org/2/library/csv.html) - a CSV handling library, to create and modify CSV data
  * [re](http://docs.python.org/2/library/re.html) - Regular expressions in Python
  * [urllib](http://docs.python.org/2/library/urllib.html) - a library to, among other things, encode a string to a URL-friend format
  * [urlparse](http://docs.python.org/2/library/urlparse.html) - something I used to revert back and encoded URL to a human-readable format 
  * [os](http://docs.python.org/2/library/os.html) - used to create, modify and save files
  * [time](http://docs.python.org/2/library/time.html) - used to time some crawler tasks
  * [random](http://docs.python.org/2/library/random.html) - for chaos

Disclaimer
----------

I did this project for a very specific purpose, which may or may not be aligned with your goals. It goes without saying that the code is not free of bugs and that it may not behave 100% correctly all the time. Google is very smart in figuring out whether you're using bots to mine data through their web interface. It also goes without saying that you're free to fork the code and edit it at your heart's content.

Also, I don't claim to be a full fledge coder. As much as I try to comment the code (sometimes too much), there are some approaches that may look far fetched or simply clumsy. 

I appreaciate comments and constructive criticism.

Contact
-------

Please use github or drop me a message at mtrpires at outlook dot com. I'm also on twitter: [@mtrpires](http://twitter.com/mtrpires)





