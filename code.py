import time
import web

from mechanize import Browser

urls = (
    '/images/(.*)', 'images', #this is where the image folder is located....
    '/(.*)', 'index'
)

web.config.debug = False

import socket
class index:
    def GET(self, rest):
        print session.session_id
        html = "<html><head></head><body>"
        if 'vote' in rest:
            codes = web.input()
            result = self.vote(codes)
            session.kill()
            html += result
        elif rest.isdigit():
            s = session
            self.get_and_display_captchas(int(rest))
            for i in range(int(rest)):
                html += "<img src='/images/%s_captcha%d.png'>" % (session.session_id, i)

            html += "<form method='GET' action='/vote'>"

            for i in range(int(rest)):
                html += "<input type='text' name='%d'><br />" % i

            html += "<input type='submit' value='enviar'></form>"
        html += "</body></html>"
        return html

    def get_and_display_captchas(self, n):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 12345))
        s.send("GET/%s/%d" % (session.session_id, n))
        if s.recv(2) == "OK":
            print "Ok..."
        s.close()

    def vote(self, codes):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 12345))
        s.send("SEND/%s/%s" % (session.session_id, ";".join([ codes[str(i)] for i in range(len(codes)) ])))
        r = s.recv(1024)
        s.close()
        return r

import os
class images:
    def GET(self,name):
        ext = name.split(".")[-1] # Gather extension

        cType = {
            "png":"images/png",
            "jpg":"image/jpeg",
            "gif":"image/gif",
            "ico":"image/x-icon"            
        }

        if name in os.listdir('images'):  # Security
            web.header("Content-Type", cType[ext]) # Set the Header
            return open('images/%s'%name,"rb").read() # Notice 'rb' for reading images
        else:
            web.notfound()

app = web.application(urls, globals())
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'))
    web.config._session = session
else:
    session = web.config._session

if __name__ == '__main__':
    app.run()
