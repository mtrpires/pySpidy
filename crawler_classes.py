# -*- coding: utf-8
# @mtrpires - http://github.com/mtrpires


class MediaObject(object):
    """
    The MediaOutletLink contains the information regarding
    the link returned by the Google Search, such as direct URL
    to the story and details about the date it was published
    """
    def __init__(self, title, date, desc, url, kind):
        """
        Initiates the object with the direct link to the story
        and the date it was published. Information comes from the
        Google Search.
        """
        self.title = title
        self.date = date
        self.desc = desc
        self.url = url
        self.kind = kind

    def getTitle(self):
        return self.title

    def getDate(self):
        return self.date

    def getDesc(self):
        return self.desc

    def getURL(self):
        return self.url

    def getKind(self):
        return self.kind

# Still don't know if I'm gonna use this...
#
# class MediaOutlet(object):
#     """
#     The MediaOutlet class contains the kind (magazine, newspaper etc),
#     name (veja, folha etc) and URL of the media outlet)
#     """
#     def __init__(self, kind, name, url):
#         """
#         Initiates the object with kind, name and URL.
#         All params are strings.
#         """
#         self.kind = kind
#         self.name = name
#         self.url = url
#
#     def getKind(self):
#         """
#         Gets the kind of the media outlet.
#         kind = string
#         Expected values are:
#         portal, revista, jornal, blog
#         """
#         return self.kind
#
#     def getName(self):
#         """
#         Gets the name of the media outlet.
#         Expected values are:
#         Terra, G1, UOL, Veja, IstoÉ, Época, Folha, O Globo,
#         Folha de S.Paulo, Estado de S.Paulo, Nassif, Simon.
#         """
#         return self.name
#
#     def getURL(self):
#         """
#         Gets the URL of the media outlet.
#         """
#         return self.url
#
#     def setKind(self, kind):
#         """
#         Sets the kind of the media outlet.
#         Expected values are:
#         portal, revista, jornal, blog
#         """
#
#         self.kind = kind
#
#     def setName(self, name):
#         """
#         Sets the name of the media outlet.
#         Expected values are:
#         Terra, G1, UOL, Veja, IstoÉ, Época, Folha, O Globo,
#         Folha de S.Paulo, Estado de S.Paulo, Nassif, Simon.
#         """
#         self.name = name
#
#     def setURL(self, url):
#         """
#         Sets the URL of the media outlet.
#         """
#         self.url = url
#
#     def __repr__(self):
#         """
#         Shows useful information about the Object when called from prompt
#         """
#         return self.getName()
