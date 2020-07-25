#!/usr/bin/python3

import urllib.request

class ParsedItem:
    def __init__(self, link=None, title=None, date=None):
        self.link=link
        self.title=title
        self.date=date

def getSource(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except Exception as e:
        print("==== GetSource ====")
        print(e)
        print("==== End ====")
        response = ""
        raise Exception

def writeToFile(output, outName):
    with open(outName, "ab") as f:
        header = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n".encode('utf-8')
        header += "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n".encode('utf-8')
        f.write(u'\ufeff'.encode('utf-8'))
        f.write(header)
        f.write(output)
        f.write("</html>".encode('utf-8'))
