import requests, json, re, word2vec, math
from scipy import spatial
import numpy
import word2vec
#from space_action import get_postagging, get_dependency

def parse_text(parser, sentence, state = None):
    parsedEx = parser(sentence)
    # extract POS tagging from the parsed response
    full_pos = get_postagging(parsedEx)
    # extract dependency tree from parsed response
    full_dep = get_dependency(parsedEx)
    return full_pos, full_dep

def get_root(full_dep):
    root_word = ''
    for each_dep in full_dep:
        if each_dep[1] == 'ROOT':
            root_word = each_dep[0].lower()
    return root_word

def getWords(data):
    return re.compile(r"[\w]+").findall(data)

def getWordsX(data):
    return re.compile(r"[\w'.]+").findall(data)

def union(t1, t2, v1, v2):
    t = []
    v = []
    for i in range(len(t1)):
        if t1[i] not in t:
            t.append(t1[i])
            v.append(v1[i])
    for i in range(len(t2)):
        if t2[i] not in t:
            t.append(t2[i])
            v.append(v2[i])
    return t, v

def flex(t):
    tminus = []
    for each in t:
        if each == "don't":
            tminus.append('do')
            tminus.append('not')
        else:
            tminus.append(each)
    return tminus

def polish(t):
    tminus = []
    remobe = ['PUNCT', 'DET']
    for each in t:
        if each[1] not in remobe:
            tminus.append(each[0])
    return tminus

def agreg(t):
    sent = ''
    for each in t:
        sent = sent + each + ' '
    return sent[:-1]

def suit_sim(b, v):
    delta = 0.6
    r = []
    #print type(b)
    for each in v:
        #print type(each)
        r.append(1 - spatial.distance.cosine(b, each))
        #print 1 - spatial.distance.cosine(b, each)
    m = max(r)
    if m > delta:
        return m
    return 0
#
# Li, Y., McLean, D., Bandar, Z. A., O'Shea, J. D., and Crockett, K. (2006)
# Sentence Similarity Based on Semantic Nets and Corpus Statistics.
# IEEE Transactions on Knowledge and Data Engineering 18, 8, 1138-1150.
#

def ssv_fast(t, t1, t2, v, v1, v2):
    s1 = []
    s2 = []
    for i in range(len(t)):
        if t[i] in t1:
            s1.append(1)
        else:
            s1.append(suit_sim(v[i], v1))
        if t[i] in t2:
            s2.append(1)
        else:
            s2.append(suit_sim(v[i], v2))
    #print 'sss ',s1, s2
    similarity = 1 - spatial.distance.cosine(s1, s2)
    return similarity

def suit_index(b, v):
    delta = 0.6
    r = []
    for each in v:
        r.append(1 - spatial.distance.cosine(b, each))
    m = max(r)
    if m > delta:
        return r.index(m) + 1
    return 0

def norm(r):
    total = 0
    for each in r:
        total = total + each*each
    return math.sqrt(total)

hashing = dict()

#
# Li, Y., McLean, D., Bandar, Z. A., O'Shea, J. D., and Crockett, K. (2006)
# Sentence Similarity Based on Semantic Nets and Corpus Statistics.
# IEEE Transactions on Knowledge and Data Engineering 18, 8, 1138-1150.
#

def wo_fast(t, t1, t2, v, v1, v2):
    delta = 0.6
    r1 = []
    r2 = []
    for i in range(len(t)):
        if t[i] in t1:
            r1.append(t1.index(t[i])+1)
        else:
            r1.append(suit_index(v[i], v1))
        if t[i] in t2:
            r2.append(t2.index(t[i])+1)
        else:
            r2.append(suit_index(v[i], v2))
    #print 'wo ', r1, r2
    r = []
    q = []
    for i in range(len(r1)):
        r.append(r1[i]-r2[i])
        q.append(r1[i]+r2[i])
    r = norm(r)
    q = norm(q)
    #print r,q
    return (1 - r/q)

def dp(t, t1, t2, d1, d2, model):
    v1 = []
    v2 = []
    for i in range(len(t1)):
        try:
            baset1 = model[t1[i]]
        except Exception, e:
            if hashing.has_key(t1[i]) == True:
                baset1 = hashing[t1[i]]
            else:
                baset1 = numpy.random.rand(100,1)
                hashing[t1[i]] = baset1
            #print "word not found v1 wo " + t1[i]
        v1.append(baset1)
    for i in range(len(t2)):
        try:
            baset2 = model[t2[i]]
        except Exception, e:
            if hashing.has_key(t2[i]) == True:
                baset2 = hashing[t2[i]]
            else:
                baset2 = numpy.random.rand(100,1)
                hashing[t2[i]] = baset2
            #print "word not found v2 wo " + t2[i]
        v2.append(baset2)
    # not the v1 and v2 have all vectors
    m1 = numpy.zeros((len(t),len(t)))
    m2 = numpy.zeros((len(t),len(t)))
    for i in range(len(t)):
        if t[i] in t1:
            m1[i][i] = 1*4
        else:
            try:
                baset = model[t[i]]
            except Exception, e:
                if hashing.has_key(t[i]) == True:
                    baset = hashing[t[i]]
                else:
                    baset = numpy.random.rand(100,1)
                    hashing[t[i]] = baset
            m1[i][i] = suit_sim(baset, v1)*4
        if t[i] in t2:
            m2[i][i] = 1*4
        else:
            try:
                baset = model[t[i]]
            except Exception, e:
                if hashing.has_key(t[i]) == True:
                    baset = hashing[t[i]]
                else:
                    baset = numpy.random.rand(100,1)
                    hashing[t[i]] = baset
            m2[i][i] = suit_sim(baset, v2)*4
    for i in range(len(d1)):
        d1[i][1] = 'DEP'
        d1[i][3] = []
        d1[i][4] = []
    for i in range(len(d2)):
        d2[i][1] = 'DEP'
        d2[i][3] = []
        d2[i][4] = []
    for i in range(len(t)):
        for j in range(len(t)):
            if [t[i],'DEP',t[j],[],[]] in d1:
                m1[i][j] = 1
                m1[j][i] = 1
            if [t[i],'DEP',t[j],[],[]] in d2:
                m2[i][j] = 1
                m2[j][i] = 1

    print m1
    print m2
    similarity_dp_cnze = 1 - float(numpy.count_nonzero(m1-m2)) / float((numpy.count_nonzero(m1) + numpy.count_nonzero(m2)))
    print 'cnze ', similarity_dp_cnze
    similarity_dp = 1 - numpy.linalg.norm(m1-m2)/(numpy.linalg.norm(m1)+numpy.linalg.norm(m2))
    print 'norm ', similarity_dp
    return similarity_dp, similarity_dp_cnze
#dp(["hello", "a","b","c"],[],[],[],[])

def advance_ssv(t, t1, t2):
    v1 = []
    v2 = []

def distance(t1,t2):
    model = word2vec.load('../latents.bin')
    sentence_1 = unicode(t1, "utf-8")
    sentence_2 = unicode(t2, "utf-8")
    t1 = getWords(t1)
    t2 = getWords(t2)
    t1 = flex(t1)
    t2 = flex(t2)
    v=[]
    v1=[]
    v2=[]

    for i in range(len(t1)):
        try:
            baset1 = model[t1[i]]
        except Exception, e:
            if hashing.has_key(t1[i]) == True:
                baset1 = hashing[t1[i]]
            else:
                baset1 = numpy.random.rand(100,1)
                hashing[t1[i]] = baset1
        v1.append(baset1)
    for i in range(len(t2)):
        try:
            baset2 = model[t2[i]]
        except Exception, e:
            if hashing.has_key(t2[i]) == True:
                baset2 = hashing[t2[i]]
            else:
                baset2 = numpy.random.rand(100,1)
                hashing[t2[i]] = baset2
        v2.append(baset2)

    t, v = union(t1, t2, v1, v2)


    #print d1
    #print d2
    #similarity_dp = dp_old(t, t1, t2, d1, d2)
    similarity_dp, similarity_dp_cnze = 0, 0
    #similarity_dp, similarity_dp_cnze = dp(t, t1, t2, d1, d2, model)
    # -------------- sementic similarity between two sentences ------- #
    similarity_ssv = ssv_fast(t, t1, t2, v, v1, v2)
    #print 'ssv ', similarity_ssv
    # ----------------- word similarity between sentences ------------ #
    similarity_wo = wo_fast(t, t1, t2, v, v1, v2)
    return similarity_ssv, similarity_wo

def test():
    #from spacy.en import English
    #parser = English()
    model = word2vec.load('../latents.bin')
    t1 = "a quick brown dog jumps over the lazy fox"
    t2 = "a fast brown fox jumps over the lazy dog"
    #t2 = "he is a brown fox"
    t2 = "what jumps over the lazy fox is a quick brown dog"
    '''t1 = "Many consider Maradona as the best player in soccer history"
    t2 = "Maradona is one of the best soccer players"
    t1="The DVD-CCA then appealed to the state Supreme Court albert. hdujhuju".lower()
    t2="The DVD CCA appealed that decision to the U.S. Supreme Court albert einstein bhijjnjd.".lower()
    t1="Amrozi accused his brother, whom he called the witness, of deliberately distorting his evidence.".lower()
    t2="Referring to him as only the witness, Amrozi accused his brother of deliberately distorting his evidence.".lower()'''
    sentence_1 = unicode(t1, "utf-8")
    #p1, d1 = parse_text(parser, sentence_1, 1)
    sentence_2 = unicode(t2, "utf-8")
    #p2, d2 = parse_text(parser, sentence_2, 1)
    t1 = getWords(t1)
    t2 = getWords(t2)
    t1 = flex(t1)
    t2 = flex(t2)
    #t1_p = polish(p1)
    #t2_p = polish(p2)
    #print t1, t1_p
    #print t2, t2_p
    #print d1
    v=[]
    v1=[]
    v2=[]

    for i in range(len(t1)):
        try:
            baset1 = model[t1[i]]
        except Exception, e:
            if hashing.has_key(t1[i]) == True:
                baset1 = hashing[t1[i]]
            else:
                baset1 = numpy.random.rand(100,1)
                hashing[t1[i]] = baset1
        v1.append(baset1)
    for i in range(len(t2)):
        try:
            baset2 = model[t2[i]]
        except Exception, e:
            if hashing.has_key(t2[i]) == True:
                baset2 = hashing[t2[i]]
            else:
                baset2 = numpy.random.rand(100,1)
                hashing[t2[i]] = baset2
        v2.append(baset2)

    t, v = union(t1, t2, v1, v2)
    print t


    #print d1
    #print d2
    #similarity_dp = dp_old(t, t1, t2, d1, d2)
    similarity_dp, similarity_dp_cnze = 0, 0
    #similarity_dp, similarity_dp_cnze = dp(t, t1, t2, d1, d2, model)
    print similarity_dp, similarity_dp_cnze
    # -------------- sementic similarity between two sentences ------- #
    similarity_ssv = ssv_fast(t, t1, t2, v, v1, v2)
    #print 'ssv ', similarity_ssv
    # ----------------- word similarity between sentences ------------ #
    similarity_wo = wo_fast(t, t1, t2, v, v1, v2)
    print similarity_ssv, similarity_wo, similarity_dp



import time
start = time.time()
test()
done = time.time()
elapsed = done - start
print '~~~~~~~~~~~~', '\n'
print distance("a quick brown dog jumps over the lazy fox", "what jumps over the lazy fox is a quick brown dog")
print 'time elapsed '

print(elapsed)
