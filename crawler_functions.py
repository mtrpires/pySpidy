# -*- coding: utf-8
#
# @mtrpires - http://github.com/mtrpires

import csv
import re
import urllib
import urlparse
import mechanize
import os

from bs4 import BeautifulSoup
from crawler_classes import MediaObject

# Googles base search URL
baseURL = "https://www.google.com/search?"


def browserInit():
    """
    Initiates browser session. Change user agent to your liking.
    returns: a browser object to be called by other functions.
    """
    br = mechanize.Browser()

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent',
                      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) \
                      Gecko/20100101 Firefox/21.0')]
    return br


def setSearchParams(site, searchTerm, dateMin, dateMax, perPage=100, start=0):
    """
    Defines Google search params
    site: ex. "veja.abril.com.br" - string

    >> If you don't want to use a specific website, please
    consider editing the code to remove the 'site:%s ' from
    the parameters.

    searchTerm = ex. "Ciencia sem fronteiras" - string
    start: from which result to start - 0, 12, 100 etc - integer
    dateMin: lower limit to search - ex. 05/31/2012 - string, US format
    dateMax: upper limit to search - ex. 12/27/2013 - string, US format
    perPage: the ammount of results per page - ex. 75,15 (max is 100) - integer

    returns: an encoded string, ready to be parsed to the browser
    """

    site = site  # example: veja.abril.com.br/noticia
    searchTerm = searchTerm  # example: 'Ciencia sem fronteiras'
    start = start  # From which result to start: '0', '100', '200' etc
    dateMin = dateMin  # example: 01/05/2012
    dateMax = dateMax  # example: 31/05/2013
    perPage = perPage  # example: 75, 100 etc - doesn't seem to work when
    # dateMin/Max are used. It's fine otherwise

    # These are some of the parameters Google uses to find pages
    queryParams = {"q": 'site:%s "%s"' % (site, searchTerm),
                   "start": "%d" % start,
                   "tbs": "cdr:1,cd_min:%s,cd_max:%s" % (dateMin, dateMax),
                   "num": "%d" % perPage,
                   }

    # urllib.urlencode converts queryParams elements into x=y& pairs
    params = urllib.urlencode(queryParams)

    return params


def downloadHTML(baseURL, params):
    """
    Downloads the HTML from Google.
    baseURL: https://google.com/search?
    Params: an encoded string from setSearchParams()

    returns: an HTML Beautiful Soup object.
    """
    HTML = browserInit().open(baseURL+params).read()
    HTMLsoup = BeautifulSoup(HTML)
    return HTMLsoup


def findContent(HTMLsoup):
    """
    Finds the relevant list of HTML elements in a
    Google Search using the soup.

    returns: a list of bs4 objects with Google results.
    """
    # <li class="g"> is where all google search results are
    contentList = HTMLsoup.find_all('li', class_="g")

    return contentList

# Deprecated - It saves a step by combining
# findContent() and downloadHTML()
# def parseGooglePage(baseURL, params):
#     HTMLSoup = downloadHTML(baseURL, params)
#     contentList = findContent(HTMLSoup)
#
#     return contentList


def findResults(HTMLsoup):
    """
    Finds the number of results in the HTMLSoup. Useful
    to define how many pages there are to advance.

    returns: an integer containing the number of results from a
    search query.
    """

    # <div id=resultStats> is where 'About xxx results (y.z seconds)' shows up
    results = HTMLsoup.find('div', id='resultStats').getText().encode('utf-8')
    # Regex looks for a number followed by 'results': ex. "312 results"
    search = re.search(r'\b\d+\sresults', results).group()
    # Strips the word 'results' out of the string.
    match = re.search(r'\d+', search).group()
    print "Found", match, "results."
    # converts the string into an integer and returns the number
    # of results
    return int(match)


def storeInfo(contentList, kind):
    """
    Creates a list of MediaObject instances containing
    relevant information about the results: title, date,
    desc, url and kind.

    Kind is the website. For example: TechCrunch, NYT etc.

    returns: a list of MediaObject objects.
    """
    # Creates an empty list
    objectList = []

    # Every element on the list is a MediaObject.
    for i in range(len(contentList)):
        # Fetches relevant information using helper functions
        title = titles(contentList)[i]
        date = dates(contentList)[i]
        desc = descs(contentList)[i]
        url = URLs(contentList)[i]
        kind = kind
        mediaObject = MediaObject(title, date, desc, url, kind)
        # Appends relevant information of this MediaObject
        # to the CSV file, in the same folder.
        appendCSV(mediaObject)
        objectList.append(mediaObject)

    return objectList


def fetchLinks(objectList):
    """
    Downloads links from Google search page. The links are fetched from
    the objectList created by storeInfo().

    returns: nothing. It saves the files in the same folder the
    script runs from.
    """
    # this will help with duplicated titles
    j = 1
    # Since each element in the objectList is also a list of
    # Google results, each element is considered a page in the
    # search routine.
    print "Iterating over", len(objectList), "pages."
    for item in objectList:
        # Iterates through the results
        for i in item:
            try:
            # Downloads the URL content from the website to 'content'
                content = urllib.urlopen(i.getURL().encode('utf-8')).read()
                # file name will look like this:
                # '9 - Markets are rising in the east - NYT.html'
                filename = str(j)+" - "+i.getTitle().encode('utf-8')
                # Removes '/' from filename.
                filename = re.search(r'[^/]*', filename).group()
                # saves in the same folder the script is run from
                path = os.path.abspath("%s.html" % (filename))
                with open(path, 'w+') as file:
                    file.write(content)
                    file.close()
                # increments the index for the file name
                j += 1
                print "Saved:", i.getURL()
            except:
                print "Could not download content."
                print "I tried this URL:", i.getURL()

    print "Links (hopefully) saved successfully. Please verify saved folder."


def numPages(results):
    """
    Calculates the number of pages to search in Google.
    """
    if results % 10 == 0:
        pages = results/10
    else:
        pages = results/10+1
    return pages


def changePage(params):
    """
    Changes the restuls page. It grabs the params
    and reverse them to a dict. The default behaviour
    is to jump 10 results per page. I've found that you
    can't set the number of results per page if you
    set a date interval.

    returns: an URL encoded string ready to be read by the browser.
    """
    # urlparse does the job of reversing the encoded url
    paramsReversed = urlparse.parse_qsl(params)
    # Then, paramsReversed is converted to a dictionary
    paramsDict = dict(paramsReversed)
    # The 'start' value is converted to an integer
    paramsDict['start'] = int(paramsDict['start'])
    # And incremented by 10, which means: "start showing
    # results from the 10th result (11, 12, 13...)"
    paramsDict['start'] += 10
    # The new parameters are encoded back to be used
    # by the browser.
    newParams = urllib.urlencode(paramsDict)

    return newParams


def createCSV():
    """
    Creates an CSV file with with elements of the
    MediaObject, with a top row of 6 elements:
    Site, Title, URL, Description, Date and Misc.
    Misc is the only column which is not populated.
    Use it to add anything that you want.

    returns: nothing. It creates the CSV file with one top row.
    """
    # This list serves as the top row of the CSV file
    csvList = ['Site', 'Title', 'URL', 'Description', 'Date', 'Misc']
    # Routine to save the file
    with open('media.csv', 'w+') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(csvList)
        csv_file.close()
    print "CSV file created successfuly."
    print


def appendCSV(mediaObject):
    """
    Appends the information of the MediaObject to the
    CSV file created by the createCSV() function.

    returns: nothing. It appends info to the CSV file.
    """
    # This list gets relevant information from the MediaObject
    csvList = [mediaObject.getKind().encode('utf-8'),
               mediaObject.getTitle().encode('utf-8'),
               mediaObject.getURL().encode('utf-8'),
               mediaObject.getDesc().encode('utf-8'),
               mediaObject.getDate(), ""]
    # Trying to save...
    try:
        with open('media.csv', 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(csvList)
            csv_file.close()
        print "Information for", mediaObject.getTitle(), "appended \
                                                         successfully \
                                                         to the CSV."
    # Not the best way to handle errors, I know.
    except:
        "Could not append CSV file."


###### Helper functions
def titles(contentList):
    """
    Creates a list of titles, from findContent().

    returns: a list with the titles.
    """
    # Creates a list that will be populated with titles
    titleList = []
    # In the Google Search the titles are the text
    # in between <a></a> tags.
    # BeautifulSoup find("a").get_text() grabs exactly that.
    for title in contentList:
        try:
            titleList.append(title.find("a").get_text())
        except:
            titleList.append("Title not found")
            print "Error: Title not found!"

    return titleList


def dates(contentList):
    """
    Creates a list of dates, from findContent().

    returns: a list with the dates.
    """
    # empty list for the dates
    dateList = []
    for date in contentList:
        try:
            # This BeautifulSoup method actually finds the description.
            # The first 12 characters are the date, hence, the slicing.
            dateList.append(date.find("span", class_="st").get_text()[:12])
        except:
            dateList.append("Date not found!")
            print "Error: Date not found!"

    return dateList


def descs(contentList):
    """
    Creates a list of descriptions, from findContent().

    returns: a list with the descriptions.
    """
    descList = []
    for desc in contentList:
        try:
            # slicing remove date and keeps the rest of the description.
            descList.append(desc.find("span", class_="st").get_text()[14:])
        except:
            descList.append("Description not found!")
            print "Error: Description not found!"

    return descList


def URLs(contentList):
    """
    Creates a list of URLs, from findContent().

    returns: a list with the URLs.
    """
    urlList = []
    for url in contentList:
        try:
            # Looks for the <a href=""> and grabs whatever's
            # in between the quotes.
            link = url.find("a").get("href")
            # Some results come with too many parameters. This
            # grabs the 'http://... &".
            try:
                address = re.search(r'http.[^&]*', link).group()
                urlList.append(address)
            except:
                urlList.append(link)
        except:
            urlList.append("Link not found!")
            print "Error: Link not found!"

    return urlList
##################
