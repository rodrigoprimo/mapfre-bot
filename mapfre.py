from mechanize import Browser
import os, socket, thread

brs = []

def get(c, d, sid, n):
    for i in range(n):
        brs.append(Browser())
        u = brs[i].open("http://www.omaiorbarbeirodobrasil.com.br/home-promocao/historia.do?id=52")
        img = brs[i].open("http://www.omaiorbarbeirodobrasil.com.br/captcha.do")
        open("images/%s_captcha%d.png" % (sid, i), 'w').write(img.read())
    d[sid] = brs
    c.send("OK")
    c.close()

def send(c, brs, codes):
    html = "<ul>"
    for i in range(min(len(brs), len(codes))):
        br = brs[i]
        r = br.open('http://www.omaiorbarbeirodobrasil.com.br/home-promocao/votar.do', data="id=52&nota=5&codigo=%s&nocacheattr=1240840177958" % codes[i]) 
        resp = r.read()
        print resp
        if "sucesso!" in resp:
            html+="<li><b>OK!</b></li>"
        else:
            html+="<li><i>FALHOU!</i></li>"
    html += "</ul><br/><br/>Total: %d <b>OK!</b> e %d <i>FALHOU!</i>" % (html.count("OK!"), html.count("FALHOU!"))
    html += "<h3><a href='/10'>Voltar</a></h3>"
    c.send(html)
    c.close()

def main():
    dic = dict()
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("127.0.0.1", 12345))
            s.listen(1)
            c, d = s.accept()
            s.close()
            print "conectou: ", d
            cmd = c.recv(1024)
            print "cmd: ", cmd
            cmd = cmd.split("/")
            print cmd[1]
            if cmd[0] == "GET":
                thread.start_new_thread(get, (c, dic, cmd[1], int(cmd[2])))
            else:
                thread.start_new_thread(send, (c, dic[cmd[1]], cmd[2].split(";")))
        except KeyboardInterrupt:
            import sys
            sys.exit()
        except Exception, e:
            print e
            c.send("FAIL")
            c.close()
            pass

main()
