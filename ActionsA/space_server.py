from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
from urlparse import urlparse, parse_qs
import json, re

from spacy.en import English
parser = English()

def getWords_special_location(data):
    return re.compile(r"[\w'/.,-@]+").findall(data)

def uniquefy(a):
    b=[]
    for i in a:
        if i not in b:
            b.append(i)
    return b

def get_ner(each_ex, parsedEx):
    #for token in parsedEx:
    #    print(token.orth_, token.ent_type_ if token.ent_type_ != "" else "(not an entity)")
    #print("-------------- entities only ---------------")
    # if you just want the entities and nothing else, you can do access the parsed examples "ents" property like this:
    lust = getWords_special_location(each_ex)
    #print (lust)
    d1 = ['i', 'live', 'in', 'please', 'hi', 'give', 'find', 'who', 'what', 'my', 'hungry', 'near', 'me', 'thank', 'you', \
            'want', 'to', 'eat', 'like','liked', 'I', 'can', 'you', 'suggest', 'of', 'is', 'are', 'near', 'there', 'some', \
            'little', 'now', 'wanna', 'want', 'at', 'on', 'in', 'near', 'area', 'next', 'and', 'how', 'about', 'or', \
            'the', 'a', 'an', 'about', 'for', 'with', 'should', 'could', 'would', 'out','time','person','year','way','day',\
            'thing','man','world','life','hand','part','child','eye','woman','place','work','week', 'doing',\
            'case','point','government','company','number','group','problem','fact','be','have','do','say',\
            'get','make','go','know','take','see','come','think','look','want','give','use','find','tell', 'telling',\
            'ask','work','seem','feel','try','leave','call','good','new','first','last','long','great','little','own','other',\
            'old','right','big','high','different','small','large','next','early','young','important','few',\
            'public','bad','same','able','to','of','in','for','on','with','at','by','from','up','about','into',\
            'over','after','beneath','under','above','the','and','a','that','I','it','not','he','as','you', \
            'this','but','his','they','her','she','or','an','will','my','one','all','would','there','their', 'talk', \
            'talking', 'love', 'loved', 'hello', 'help', 'helping', 'helped', 'pleasure', 'bye', 'goodbye', 'care', 'later', \
            'no','nothing', 'thanks', 'welcome', 'something', 'hey', 'am', 'month','year','week','day','hour','minute','min','second', \
            'months','years','weeks','days','hours','minutes','mins','seconds','time', 'today', 'tomorrow', 'am', 'pm',\
            'january', 'febuary', 'marth', 'april', 'may', 'june', 'july','august', 'september', 'october', 'november', 'december', \
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','km', 'kilometer', 'kilometers', 'meter', 'm',\
            'cm', 'kms', 'miles', 'yards', 'feet', 'feets','evening', 'morning', 'afternoon', 'noon', 'night', 'looking']
    #d1 = []
    kiss = ''
    bang = ''
    bump_last = ['.', ',', ';', ':', '(', ')', '?', '!']
    for c_cmall in lust:
        if c_cmall[-1] not in bump_last:
            if c_cmall not in d1:
                kiss = kiss + c_cmall.title() + ' '
                bang = bang + c_cmall.title() + ' '
            else:
                kiss = kiss + c_cmall + ' '
                bang = bang + c_cmall + ' '
        else:
            if c_cmall not in d1:
                kiss = kiss + c_cmall[:-1].title() + ' '
                bang = bang + c_cmall[:-1].title() + ' ' + c_cmall[-1] + ' '
            else:
                kiss = kiss + c_cmall[:-1] + ' '
                bang = bang + c_cmall[:-1] + ' ' + c_cmall[-1] + ' '
    if type(bang) == type('str'):
        bang = unicode(bang, "utf-8")
    parsedEx_loc = parser(bang)
    ents = list(parsedEx.ents)
    full_ents = []
    for entity in ents:
        full_ents.append([entity.label, entity.label_, ' '.join(t.orth_ for t in entity)])
    ents = list(parsedEx_loc.ents)
    for entity in ents:
        full_ents.append([entity.label, entity.label_, ' '.join(t.orth_ for t in entity)])
    full_ents = uniquefy(full_ents)
    return full_ents

def get_postagging(parsedData):
    full_pos = []
    sent = []
    for span in parsedData.sents:
        sent = sent + [parsedData[i] for i in range(span.start, span.end)]
        #break

    for token in sent:
        full_pos.append([token.orth_, token.pos_])
    return full_pos

def get_dependency(parsedEx):
    # Let's look at the dependencies of this example:
    # shown as: original token, dependency tag, head word, left dependents, right dependents
    full_dep = []
    for token in parsedEx:
        full_dep.append([token.orth_, token.dep_, token.head.orth_, [t.orth_ for t in token.lefts], [t.orth_ for t in token.rights]])
    return full_dep

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        if self.path == '/beatle/':
            self.wfile.write(parse_qs(urlparse(self.path).query))
            return
        each_ex = parse_qs(urlparse(self.path).query)
        if each_ex == {}:
            return
        each_ex = each_ex['message'][0]
        if type(each_ex) == type('str'):
            each_ex = unicode(each_ex, "utf-8")
        parsedEx = parser(each_ex)
        full_pos = get_postagging(parsedEx)
        full_dep = get_dependency(parsedEx)
        full_ents = get_ner(each_ex, parsedEx)
        power = {"full_pos":full_pos, "full_dep":full_dep, "full_ents":full_ents}
        self.wfile.write(json.dumps(power))
        return

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
