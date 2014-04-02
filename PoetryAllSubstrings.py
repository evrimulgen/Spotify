from Spotify import *
import sys
import string

s = Spotify()

cachedTerms = dict()

def doSearch(search_term):
    print(search_term, end='')
    if search_term not in cachedTerms:
        this_result = json.loads(s.trackSearch(search_term))
    else:
        print('.already tried')
        return {'search_term':search_term},False
    
    success = True
    if this_result['num_results'] == 0:
        success = False
        cachedTerms[search_term] = False
        
    return this_result,success

def findAllSubstrings(words):
    phrase_length = len(words)
    phrases = []
    for l in range(1,len(words)+1):
        for i in range(0,len(words)-l+1):
            phrases.append(words[i:i+l])
    phrases = phrases[::-1]
    print(phrases)

def displayResults(res):
    idxs = []
    search_phrase = phrase
    for i in range(0,len(res)):
        # To display them in the correct order, find the index of where each successful search_term is in the phrase
        idxs.append(search_phrase.find(res[i]['search_term']))
        search_phrase = re.sub(res[i]['search_term'], '_'*len(res[i]['search_term']), search_phrase, count=1)

    for i in range(0,len(res)):
        idx = idxs.index(min(idxs))
        idxs[idx] = float('inf')
        x = res[idx]['max_pop_idx']
        print('{0:4} {1:20} {2:25} {3:10}'.format(
            res[idx]['items'][x]['popularity'],
            res[idx]['items'][x]['title'],
            res[idx]['items'][x]['artist'],
            res[idx]['items'][x]['album'])
              )
    
punct = re.sub('\'', '', string.punctuation)
phrase = ' '.join(sys.argv[1:])
phrase = re.sub('[' + punct + ']', '', phrase)
words = phrase.split(' ')

res = []

findAllSubstrings(words)
