from Spotify import *
import sys
import string

def doSearch(search_term):
    print(search_term, end='')
    this_result = json.loads(s.trackSearch(search_term))
    success = True
    if this_result['num_results'] == 0:
        success = False
    return this_result,success

s = Spotify()

punct = re.sub('\'', '', string.punctuation)
phrase = ' '.join(sys.argv[1:])
phrase = re.sub('[' + punct + ']', '', phrase)
words = phrase.split(' ')

res = []
i = len(words)-1
idx_last_added = -1
need_to_pop = False
added_post_word = False
search_term = ''
while i >= 0:
    this_result = []
    # start with the last single word
    search_term = words[i]
    this_result,success = doSearch(search_term)
    while not success:
        # Add on the word before it
        i = i - 1
        if i < 0:
            break
        search_term = words[i] + ' ' + search_term
        this_result,success = doSearch(search_term)
        if not success and not added_post_word:
            # add on the word after if it was a single word title
            # and delete that one from the list of results
            # Do this because the word is likely to be a noun
            search_term = search_term + ' ' + words[idx_last_added]
            need_to_pop = True
            this_result,success = doSearch(search_term)
            added_post_word = True

        if not success and i <= 0:
            # Try the whole phrase as a last resort
            search_term = phrase
            this_result,success = doSearch(search_term)

            j = idx_last_added+1
            need_to_pop = True
            search_term = ' '.join(words[0:j])
            this_result,success = doSearch(search_term)
            while not success and j >= 0:
                need_to_pop = False
                # Start trimming the search term from the other direction
                j = j - 1
                search_term = ' '.join(words[0:j])
                this_result,success = doSearch(search_term)

            if this_result['num_results'] != 0:
                # We found a match, now go back and try to add the words we haven't matched yet
                words = words[j:idx_last_added]
                phrase = ' '.join(words)
                print(words)
                i = len(words)-1
            else:
                break
            
    if need_to_pop:
        res.pop()
        idx_last_added = -1
        need_to_pop = False
        
    if len(search_term.split(' ')) == 1:
        idx_last_added = i
    else:
        idx_last_added = -1
    i = i - 1
    if this_result['num_results'] != 0:
        res.append(this_result)

for i in range(len(res)-1,-1,-1):
    x = res[i]['max_pop_idx']
    print('{0:4} {1:20} {2:25} {3:10}'.format(
        res[i]['items'][x]['popularity'],
        res[i]['items'][x]['title'],
        res[i]['items'][x]['artist'],
        res[i]['items'][x]['album'])
          )
