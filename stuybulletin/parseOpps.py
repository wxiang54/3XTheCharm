from PyPDF2 import PdfFileReader
from pprint import pprint
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.application import create_app, get_config
from app.extensions import db
from app.models.opportunities import Opportunity

DATA_DIR = "app/testing_data/"

'''
Current Bugs:
* I probably missed a keyword or two, but i think its aii
* Some names are > 1 line, which screws up my algo bc it only takes the one line before "Details: "
'''
### GLOBALS ###
#files = ["opp1.pdf", "opp2.pdf", "opp3.pdf"]
files = ["opp2.pdf"]
keywords = ["Additional Information", "Schedule of Programs", "List of Academy Locations", "Website", "Application", "Contact", "Contact Information", "Email", "Duration", "Eligibility", "Deadline"]
oppList = []

def getNextKwdIndex(splitted, lineNum):
    for line in [x + lineNum + 1 for x in xrange(len(splitted[lineNum+1:]))]:
        indexList = [line for kwd in keywords if kwd in splitted[line]]
        if indexList:
            nextKwdIndex = min(indexList)
            return nextKwdIndex
    return -1

def parsePDF(filename):
    f = PdfFileReader(open(filename, "rb"))
    # print how many pages input1 has:
    print "%s has %d pages." % (filename, f.getNumPages())
    
    #start from page 2 (0 is title, 1 is ToC, 2-3 are general opp links)
    numPages = f.getNumPages() - 4
    for pageNum in [x+4 for x in xrange(numPages)]:
        pageObj = f.getPage(pageNum)
        pageObj.compressContentStreams()
        pageText = pageObj.extractText().strip()
        splitted = pageText.split('\n')[1:] #first line is page num
        
        #fix dumb syntactical things
        lineNum = 0
        while lineNum < len(splitted):
            if splitted[lineNum] == '-':
                splitted[lineNum-1] += '-' + splitted[lineNum+1]
                splitted.pop(lineNum)
                splitted.pop(lineNum) #lineNum+1 becomes lineNum after first pop
            elif splitted[lineNum] in ['', ' ']:
                splitted.pop(lineNum)
            else:
                lineNum += 1
                
        #pass 2: parse opps
        currentOpp = {}
        for lineNum in xrange(len(splitted)):
            if "Details:" in splitted[lineNum]: #opp has been located, YEET
                #refresh currentOpp
                oppList.append(currentOpp)
                currentOpp = {}
                currentOpp["Name"] = splitted[lineNum-1]
                nextKwdIndex = getNextKwdIndex(splitted, lineNum)
                if nextKwdIndex == -1:
                    nextKwdIndex = len(splitted)
                currentOpp["Details"] = reduce(lambda x,y: x.strip() + ' ' + y.strip()if len(y)<3 else x+y, splitted[lineNum+1:nextKwdIndex]) #dont ask
            elif splitted[lineNum].strip() in keywords: #if its a keyword other than "Details:"
                if "Name" in currentOpp and currentOpp["Name"] == "AIDS WALK":
                    print splitted[lineNum: lineNum+10]
#                   print splitted[nextKwdIndex]
                nextKwdIndex = getNextKwdIndex(splitted, lineNum)
                if "Details:" in splitted[nextKwdIndex]:
                    nextKwdIndex -= 1 #dont include the title of the next opp
                elif nextKwdIndex == -1:
                    nextKwdIndex = len(splitted)
                currentOpp[splitted[lineNum].strip(': ')] = reduce(lambda x,y: x.strip() + ' ' + y.strip()if len(y)<3 else x+y, splitted[lineNum+1:nextKwdIndex]) #dont ask



                
if __name__ == "__main__":
    app = create_app(get_config('app.config.Production'))
    app.app_context().push()
    for filename in files:
        parsePDF(DATA_DIR + filename)
    for opp in oppList:
#        print "\n" * 2 + str(opp)
        
        if not opp or "Name" not in opp or "Details" not in opp:
            continue
        o = Opportunity(name = opp["Name"], description = opp["Details"])
        #initialize
        o.details = ""
        o.link = ""
        o.organization = ""
        o.required_materials = []
        o.deadline = ""
        
        if "Additional Information" in opp:
            o.details += "\nAdditional Information: " + opp["Additional Information"]
        if "Schedule of Programs" in opp:
            o.details += "\nSchedule of Programs: " + opp["Schedule of Programs"]
        if "List of Academy Locations" in opp:
            o.details += "\nList of Academy Locations: " + opp["List of Academy Locations"]
        if "Website" in opp:
            o.link += "\n" + opp["Website"]
        if "Application" in opp:
            o.link += "\n" + opp["Application"]
        if "Contact" in opp:
            o.organization += "\n" + opp["Contact"]
        if "Contact Information" in opp:
            o.organization += "\n" + opp["Contact Information"]
        if "Email" in opp:
            o.organization += "\n" + opp["Email"]
        #skip duration for now cuz its weird
        if "Eligibility" in opp:
            o.required_materials = [opp["Eligibility"]]
        if "Deadline" in opp:
            o.deadline = opp["Deadline"]
        #print "added opp: %s" % o.name
        db.session.add(o)
    db.session.commit()  
#    pprint(getAllOpportunities())
