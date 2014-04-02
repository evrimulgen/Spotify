from Spotify import *
import sys
import string

s = Spotify()

cachedTerms = dict()

def doSearch(search_term):
    if search_term not in cachedTerms:
        print(search_term, end='')
        this_result = json.loads(s.trackSearch(search_term))
    else:
        return {'search_term':search_term},False
    
    success = True
    if this_result['num_results'] == 0:
        success = False
        cachedTerms[search_term] = False
        
    return this_result,success

def iterativeSearchRemoveLast(words):
    i = len(words)-1
    success = False
    while not success and i > 0:
        # remove last word until we reach the last word
        this_result,success = doSearch(' '.join(words[:i]))
        i = i - 1
    return this_result,success

def iterativeSearchRemoveFirst(words):
    i = 1
    success = False
    while not success and i < len(words):
        # remove first word until we reach the last word
        this_result,success = doSearch(' '.join(words[i:]))
        i = i + 1
    return this_result,success
                               
def getLongestSubPhrase(words, direction):
    # start with the whole phrase
    this_result,success = doSearch(' '.join(words))
    if not success and direction == 1 and len(words)>1:
        this_result,success = iterativeSearchRemoveLast(words)
        if success: return this_result,success
        this_result,success = iterativeSearchRemoveFirst(words)
            
    elif not success and direction == -1:
        this_result,success = iterativeSearchRemoveFirst(words)
        if success: return this_result,success
        this_result,success = iterativeSearchRemoveLast(words)

    return this_result,success

def findTitles(words, res, direction):
    success = True
    unmatched_words = words
    phrase = ' '.join(words)
    while len(words) > 0 and success:
        this_result,success = getLongestSubPhrase(words, direction)
        if success:
            res.append(this_result)
            unmatched_words = re.sub(this_result['search_term'], '', ' '.join(words)).rstrip().lstrip().split(' ')
            unmatched_words = list(filter(None, unmatched_words))
        # repeat with found words removed
        phrase = re.sub(this_result['search_term'], '', phrase, count=1, flags=re.IGNORECASE).rstrip().lstrip()
        words = list(filter(None, phrase.split(' ')))

    return success,unmatched_words
    
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

direction = 1
all_words_matched = True
success,unmatched_words = findTitles(words, res, direction)

while len(res) > 0 and len(unmatched_words) > 0:
    x = res.pop(0)
    if phrase.find(x['search_term']) > phrase.find(' '.join(unmatched_words)):
        # words are out of order, we've exhausted possibilities
        res.append(x)
        break

    new_words = (x['search_term'] + ' ' + ' '.join(unmatched_words)).split(' ')
    if words == new_words:
        # we're just trying the same thing again so exit
        res.append(x)
        break

    words = new_words
    direction = direction * -1
    success,unmatched_words = findTitles(words, res, 1)

while len(unmatched_words) > 0:
    all_words_matched = False
    unmatched_words.pop(0)
    success,unmatched_words = findTitles(unmatched_words, res, 1)

print()
if not all_words_matched:
    print('I couldn\'t make the complete phrase, here\'s the best I could do')
    print()
    
displayResults(res)

