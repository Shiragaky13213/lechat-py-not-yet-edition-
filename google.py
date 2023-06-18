from bs4 import BeautifulSoup
from datetime import date
import http.client
import threading
import requests
import urllib3
import socks
import time
import re
from getpass import getpass

# function to get nc and post id
def get_values(url_post, header, proxy):
    try:
        page = requests.get(url_post, headers=header, proxies=proxy)
    except(NetworkErrors):
        pass
    else:
        soup = BeautifulSoup(page.content, 'html.parser')
        nc = soup.find('input', {'type': 'hidden', 'name': 'nc'})['value']
        postid = soup.find('input', {'type': 'hidden', 'name': 'postid'})['value']
        return nc, postid

# function to delete all messages
def delete_all(url_post, header, proxy):
    nc, postid = get_values(url_post, header, proxy)
    data = {"action" : 'delete',
            "session" : session,
            "nc" : nc,
            "postid" : postid,
            "what" : 'all'}
    page = requests.post(url_post, headers=header, proxies=proxy, data=data)
    time.sleep(1)
    data = {'action' : 'delete',
            'confirm' : 'yes',
            'session' : session,
            'nc' : nc,
            'what' : 'all'}
    page = requests.post(url_post, headers=header, proxies=proxy, data=data)

# what is
def get_meaning(header, proxy, word):
    current_time = time.ctime()[11:19]
    print(current_time, "Searching word", msgtosearch, "on Urban Dictionary")
    try:
        page = requests.get("https://www.urbandictionary.com/define.php?term="+word, headers=header, proxies=proxy)
    except(NetworkErrors):
        pass
    else:
        soupf = BeautifulSoup(page.content, 'html.parser')
        soup = BeautifulSoup(str(soupf).replace("<br/>", "\n"), 'html.parser')
        # if there is a meaning on urban dictionary, get it
        if soup.find('div', {'class': 'meaning'}):
            meaning = soup.find('div', {'class': 'meaning'}).get_text()
            if soup.find('div', {'class': 'example'}):
                example = soup.find('div', {'class': 'example'}).get_text()
                if example != "":
                    if "\n" in example:
                        reply = meaning+"\nExample:\n"+example
                    else:
                        reply = meaning+"\nExample: "+example
                else:
                    reply = meaning
            else:
                reply = meaning
        # if there is not a meaning on urban dictionary, try
        # looking on Dictionary.com
        else:
            current_time = time.ctime()[11:19]
            print(current_time, "Not found. Searching on Dictionary.com")
            try:
                page = requests.get("https://www.dictionary.com/browse/"+word, headers=header, proxies=proxy)
            except(NetworkErrors):
                pass
            else:
                soup = BeautifulSoup(page.content, 'html.parser')
                if soup.find('span', {'class': 'one-click-content css-nnyc96 e1q3nk1v1'}):
                    reply = soup.find_all('span', {'class': 'one-click-content css-nnyc96 e1q3nk1v1'}).get_text()
                # if there is not a meaning on Dictionary.com,
                # send shrugs
                else:
                    current_time = time.ctime()[11:19]
                    print(current_time, "Not found")
                    reply = "¯\_(ツ)_/¯"
        return reply

# function to get language URL to translate making a GET request
def get_lanlink(header, proxy, language):
    try:
        page = requests.get("https://translate.google.com/m?sl=auto&tl=en&mui=tl&hl=en-US", headers=header, proxies=proxy)
    except(NetworkErrors):
        pass
    else:
        soup = BeautifulSoup(page.content, 'html.parser')
        lanlink = ""
        for x in soup.find_all('div', {'class': 'language-item'}):
                if language in x.get_text().lower():
                    lanlink = x.find('a')['href'][1:]
        if lanlink != "":
            lanlink = lanlink[1:]
            return lanlink
        else:
            return False

# translate
def translate(header, proxy, words, language):
    # if there is the language on google translator, translate
    if get_lanlink(header, proxy, language):
        lanlink = get_lanlink(header, proxy, language)
        url = 'https://translate.google.com/'+lanlink+"&q="+words
        try:
            page = requests.get(url, headers=header, proxies=proxy)
        except(NetworkErrors):
            pass
        else:
            soup = BeautifulSoup(page.content, 'html.parser')
            reply = soup.find('div', {'class': 'result-container'}).get_text()
    # else, dont
    else:
        reply = "What the fuck is "+language+"?"
    return reply

# search
def search(header, proxy, what):
    data = {'q': what, 'b': ''}
    try:
        page = requests.post("https://html.duckduckgo.com/html/", headers=header, proxies=proxy, data=data)
    except(NetworkErrors):
        pass
    else:
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            replyurl = soup.find('a', {'class': 'result__a'})['href']
            replytext = soup.find('a', {'class': 'result__a'}).get_text()
        except(TypeError):
            reply = "No results."
        else:
            reply = replytext+" - "+replyurl
        return reply

# current time
def get_current_time(header, proxy, where):
    try:
        page = requests.get("https://time.is/"+where, headers=header, proxies=proxy)
    except(NetworkErrors):
        pass
    else:
        soup = BeautifulSoup(page.content, 'html.parser')
        currtime = soup.find('time').get_text()
        print(currtime)
        # strip seconds from time
        if "M" in currtime:
            reply = currtime[:5] + " " + currtime[-2:]
        else:
            reply = currtime[:5]
        return reply

# weather
def get_weather(header, proxy, where):
    try:
        page = requests.get("https://wttr.in/"+where, headers=header, proxies=proxy)
    except(NetworkErrors):
        pass
    else:
        soup = BeautifulSoup(page.content, 'html.parser')
        # if found location, get weather
        if "UNKNOWN LOCATION" not in soup.get_text():
            state = soup.find('pre').get_text().splitlines()[3][16:]
            celsius = soup.find('pre').get_text().splitlines()[4][16:]
            """if "(" not in celsius:
                num = int(celsius.split()[0])
                fahrenheit = (num * 1.8) + 32"""
            reply = state+", "+celsius#+" | "+fahrenheit
        else:
            reply = "¯\_(ツ)_/¯"
        return reply

# keep alive function
def send_keep_alive(url_post, header, proxy):
    while True:
        # wait 30 minutes
        time.sleep(1800)
        try:
            # get nc and postid
            nc, postid = get_values(url_post, header, proxy)
        except(TypeError):
            pass
        else:
            data = {'lang': 'en',
                    'nc': nc,
                    'action': 'post',
                    'session': session,
                    'postid': postid,
                    'message': 'test',
                    'sendto': '0-Commands-0'}
            current_time = time.ctime()[11:19]
            print(current_time, "Sending keep-alive...")
            try:
                # make POST request
                page = requests.post(url_post, headers=header, proxies=proxy, data=data)
            except(NetworkErrors):
                pass

# function to shorten replies
def shorten_reply(reply, lines):
    # strip blank lines
    reply = reply.replace('\n\n', '')

    # if reply is still longer than maximum of lines, strip example
    if reply.count('\n') > lines:
        for x in range(0, reply.count('\n')):
            if reply.splitlines()[x].startswith("Example:"):
                endline = x
        reply = '\n'.join(reply.splitlines()[:endline])
    # if reply is still longer than the maximum of lines, make the whole
    # reply one line
    if reply.count('\n') > lines:
        reply = reply.replace('\n', ' ')
    return reply

if __name__ == "__main__":
    action = input("Login[1] or session[2]? ")
    url = "http://danschat356lctri3zavzh6fbxg2a7lo6z3etgkctzzpspewu7zdsaqd.onion/"
    session = input("Session: ")

    url_view = url+"?action=view&session="+session
    url_post = url+"?action=post&session="+session

    header = headers("login")

    logpath = './google.txt'
    text = ""

    threading.Thread(target=send_keep_alive, args=(url_post, header, proxy)).start()
    while True:
        try:
            page = requests.get(url_view, headers=header, proxies=proxy)
        except(NetworkErrors):
            pass
        else:
            soupf = BeautifulSoup(page.content, 'html.parser')
            soup = BeautifulSoup(str(soupf).replace("<br/>", "\n"), 'html.parser')
            for x in soup.find_all('div', {'class': 'msg'})[5::-1]:
                msg = x.get_text()
                if msg in text:
                    pass
                else:
                    text = text + msg
                    reply = ""
                    sendto = ""
                    if re.match("\[\w+ to Google\]", ' '.join(msg.split()[3:6])):
                        who = re.search('\[(\w+)', msg).group(1)
                        current_time = time.ctime()[11:19]
                        print(current_time, who + " PM'd. Message:\n" + msg)
                        file = open(logpath, 'a+')
                        file.write(msg+"\n")
                        file.close()
                    try:
                        msg.split()[5]
                    except(IndexError):
                        pass
                    else:
                        who = msg.split()[3]
                        if msg.split()[5].lower() == "@google" and who != "Google":
                            try:
                                msg.split()[6]
                            except(IndexError):
                                pass
                            else:
                                if re.match('[0-9]{2}-[0-9]{2}', msg.split()[6]) and re.match('[0-9]{2}:[0-9]{2}:[0-9]{2}', msg.split()[7]) == ":":
                                    timestamp = ' '.join(msg.split()[6:8])
                                    print("Searching message by timestamp")
                                    for x in soup.find_all('div', {'class', 'msg'}):
                                        if ' '.join(x.split()[6:8]) == timestamp:
                                            msg = x.get_text()
                                if ' '.join(msg.split()[6:8]).lower() == "what is":
                                    try:
                                        msg.split()[8]
                                    except(IndexError):
                                        pass
                                    else:
                                        msgtosearch = ' '.join(msg.split()[8:])
                                        if msgtosearch.endswith('?'):
                                            msgtosearch = msgtosearch.replace(msgtosearch[-1], "")
                                        current_time = time.ctime()[11:19]
                                        reply = get_meaning(header, proxy, msgtosearch)
                                elif msg.split()[6].lower() == "translate":
                                    if msg.split()[7].startswith("'") or msg.split()[7].startswith('"'):
                                        startlen = msg.find("'") if "'" in msg else msg.find('"')
                                        endlen = msg.rfind("'") if "'" in msg else msg.rfind('"')
                                        words = msg[startlen:stoplen]
                                        if "to" in msg.split()[-2] and msg.split()[-2].isalpha():
                                            language = msg.split()[-1].lower()
                                        else:
                                            language = "english"
                                    else:
                                        if re.match('[0-9]{2}-[0-9]{2}', msg.split()[7]):
                                            try:
                                                msg.split()[8]
                                            except(IndexError):
                                                pass
                                            else:
                                                if re.match('[0-9]{2}:[0-9]{2}:[0-9]{2}', msg.split()[8]):
                                                    timestamp = ' '.join(msg.split()[7:9])
                                                    for x in soup.find_all('div', {'class': 'msg'}):
                                                        m = x.get_text()
                                                        if ' '.join(m.split()[0:2]) == timestamp:
                                                            words = ' '.join(m.split()[5:])
                                                    if not re.match('[0-9]{2}:[0-9]{2}', msg.split()[-2]) and "to" in msg.split()[-2]:
                                                        language = msg.split()[-1]
                                                    else:
                                                        language = "english"
                                        else:
                                            words = ' '.join(msg.split()[7:])
                                            language = "english"
                                    current_time = time.ctime()[11:19]
                                    print(current_time, "Translating", words, "to", language)
                                    reply = translate(header, proxy, words, language)
                                elif who == "piroc" and ' '.join(msg.split()[6:8]).lower() == "kill yourself":
                                    current_time = time.ctime()[11:19]
                                    nc, postid = get_values(url_post, header, proxy)
                                    data = {'lang': 'en',
                                            'nc': nc,
                                            'action': 'post',
                                            'session': session,
                                            'message': '',
                                            'sendto': 's *'}
                                    print(current_time, "Killing myself")
                                    try:
                                        page = requests.post(url_post, headers=header, proxies=proxy, data=data)
                                    except(NetworkErrors):
                                        pass
                                    else:
                                        exit()
                                elif who == "piroc" and "spam" in msg:
                                    current_time = time.ctime()[11:19]
                                    print(current_time, "Deleting all the messages")
                                    delete_all(url_post, header, proxy)
                                    current_time = time.ctime()[11:19]
                                    print(current_time, "Sending sorry")
                                    reply = "Sorry."
                                elif who == "piroc" and ' '.join(msg.split()[6:8]) == "niggers around":
                                    current_time = time.ctime()[11:19]
                                    print(current_time, "NIGGERS AROUND! NIGGERS AROUND!")
                                    delete_all(url_post, header, proxy)
                                    nc, postid = get_values(url_post, header, proxy)
                                    msg = "*Hides*"
                                    data = {'lang': 'en',
                                            'nc': nc,
                                            'action': 'post',
                                            'session': session,
                                            'postid': postid,
                                            'message': msg,
                                            'sendto': 's *'}
                                    try:
                                        page = requests.post(url_post, headers=header, proxies=proxy, data=data)
                                    except(NetworkErrors):
                                        pass
                                    else:
                                        data = {"action" : 'logout',
                                                "session" : session}
                                        try:
                                            page = requests.post(url_post, headers=header, proxies=proxy, data=data)
                                        except(NetworkErrors):
                                            pass
                                        else:
                                            exit()
                                elif msg.split()[6].lower() == "search":
                                    words = ' '.join(msg.split()[7:])
                                    current_time = time.ctime()[11:19]
                                    print(current_time, "Searching", words)
                                    reply = search(header, proxy, words)
                                elif ' '.join(msg.split()[6:8]).lower() == "current time":
                                    current_time = time.ctime()[11:19]
                                    where = msg.split()[-1]
                                    print(current_time, "Searching the current time in", where)
                                    reply = get_current_time(header, proxy, where)
                                elif msg.split()[6].lower() == "weather":
                                    try:
                                        msg.split()[8]
                                    except(NetworkErrors):
                                        pass
                                    else:
                                        current_time = time.ctime()[11:19]
                                        where = ' '.join(msg.split()[8:])
                                        print(current_time, "Searching the weather in", where)
                                        reply = get_weather(header, proxy, where)

                                if reply != "":
                                    quote = '@'+who
                                    nc, postid = get_values(url_post, header, proxy)
                                    if sendto == "":
                                        sendto = "s *"
                                    data = {'lang': 'en',
                                            'nc': nc,
                                            'action': 'post',
                                            'session': session,
                                            'postid': postid}
                                    if '\n' in reply:
                                        reply = quote+'\n'+reply
                                        if reply.count('\n') >= 8:
                                            reply = shorten_reply(reply, 8)
                                        data.update({'multi': 'on'})
                                    else:
                                        reply = quote+' '+reply
                                    data.update({'message': reply, 'sendto': sendto})
                                    current_time = time.ctime()[11:19]
                                    if reply != "":
                                        print(current_time, "Reply:", reply)
                                        try:
                                            page = requests.post(url_post, headers=header, proxies=proxy, data=data)
                                        except(NetworkErrors):
                                            pass
