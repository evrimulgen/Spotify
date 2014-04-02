from requester import *
import re

class Spotify:

    def trackSearch(self, track):
        page = 1
        args = {}
        args['type'] = 'track'
        args['terms'] = track
        args['page'] = page
        res = json.loads(requester().perform(requester().search, args))
        num_results = min(res['info']['limit'], res['info']['num_results'])

        # Only return exact matches and only need title/artist/album
        items = []
        max_pop = 0
        max_pop_idx = 0
        while len(items)==0 and page < 5:
            for x in range(0, num_results-1):
                
                if re.match('^' + track + '$', res['tracks'][x]['name'], flags=re.IGNORECASE):
                    title = res['tracks'][x]['name']
                    artist = res['tracks'][x]['artists'][0]['name']
                    album = res['tracks'][x]['album']['name']
                    pop = res['tracks'][x]['popularity']
                    if float(pop) > max_pop:
                        max_pop = float(pop)
                        max_pop_idx = len(items)
                    items.append({'title':title, 'artist':artist, 'album':album, 'popularity':pop})

            page = page + 1
            args['page'] = page
            res = json.loads(requester().perform(requester().search, args))
            num_results = len(res['tracks'])

        final_results = {'search_term':track, 'max_pop':max_pop, 'max_pop_idx':max_pop_idx, 'num_results':len(items), 'items':items}
        if len(items)>0:
            print(' - found')
        else:
            print(' - not found')
        return json.dumps(final_results)
