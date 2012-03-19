"""
    Copyright 2012 Nabil Tewolde

    This file is part of Like List.
    
    Like List is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from mako.template import Template
from mako.lookup import TemplateLookup
from django.utils import simplejson as json
import urllib2
from google.appengine.api import urlfetch
import urlparse
from google.appengine.api import urlfetch
import logging
from xml.dom import minidom
import oembed
import oembed_client
import formencode
import formschema

YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'
YOUTUBE_USER_EVENT_SCHEMA = 'http://gdata.youtube.com/schemas/2007/userevents.cat'
YOUTUBE_EVENTS = ['video_uploaded', 'video_rated', 'video_shared', 'video_favorited']

# not used right now
# GPLUS_API_KEY = 'YOUR_G+_API_KEY';

# For testing
# GPLUS_USER_ID = '107782897095222173836'; # Nabil's ID
# 'plus/v1/people/' + GPLUS_USER_ID + '/activities/public'
# 'http://gdata.youtube.com/feeds/api/users/wonderfalls2/events?v=2&key=' + YOUTUBE_API_KEY

oEmbedClient = oembed_client.OEmbedClient()

def getUrl(url):
    
    result = ''
    try:
        result = urlfetch.fetch(url, method=urlfetch.GET, deadline=3)
    except urlfetch.DownloadError, e:
        logging.error( "Error: %s", e )
        return None
    except Exception, e:
        logging.error( "Error: %s", e )
        return None

    return result

def getYouTubeEvents(user):
    
    url = 'http://gdata.youtube.com/feeds/api/users/%s/events?v=2&key=%s' % (user,YOUTUBE_API_KEY)
    result = getUrl(url)
    if not result:
        return []
        
    dom = minidom.parseString( result.content )

    youtube_events = []    
    youtube_feed_ulrs = []
    rpcs = []
    
    nodelist = dom.getElementsByTagName('entry')
    for numOfEvents, node in enumerate(nodelist):
        cat = node.getElementsByTagName('category')
        for cat_attr in cat:
            if cat_attr.getAttribute('scheme') == YOUTUBE_USER_EVENT_SCHEMA:                    
                youtube_action = cat_attr.getAttribute('term')
                youtube_video = node.getElementsByTagName('yt:videoid')
                if youtube_action in YOUTUBE_EVENTS and len(youtube_video) > 0:
                    youtube_video = youtube_video[0].childNodes[0].data
                                        
                    url = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=jsonc' % youtube_video
                    rpc = urlfetch.create_rpc()
                    urlfetch.make_fetch_call(rpc, url)
                    rpcs.append( (rpc, youtube_action, youtube_video) )
                    

    for rpc in rpcs:
        result = rpc[0].get_result()
        youtube_action = rpc[1]
        youtube_video = rpc[2]
        
        if not result: continue
        #logging.debug("%s", result)
        
        video_info = json.loads(result.content).get('data')

        media = [{
            'type': 'video',
            'html': '<iframe class="youtube-player" type="text/html" width="640" height="385" src="http://www.youtube.com/embed/%s" frameborder="0"></iframe>' % youtube_video,
            'display_url': 'http://youtu.be/' + youtube_video,
            'service_url': video_info['player']['default'],
            'thumbnail_url': video_info['thumbnail']['hqDefault'],            
            'provider_name': 'YouTube',
            'provider_url': 'htttp://youtube.com'
            }]
        
        video_data = {
            'service': 'youtube',
            'title': video_info['title'],
            'user_url': 'http://www.youtube.com/' + video_info['uploader'],            
            'user_name': video_info['uploader'],
            'screen_name': video_info['uploader'],
            'media': media,
            'urls': [],
            'share_action': youtube_action.replace("video_", ""),
            'created_at': video_info['uploaded']                  
            }
        
        youtube_events.append( video_data )

    return youtube_events

# https://www.googleapis.com/plus/v1/people/107782897095222173836/?key=AIzaSyAyMmHmknaIlc2f4qp37925-67nzGi5fF0
def getGooglePlusOnes(userID):
    url = 'https://www.googleapis.com/plus/v1/people/' + userID + '/activities/public?key=' + GPLUS_API_KEY    
    result = getUrl(url)
    if not result:
        return []
    
    #logging.debug(" %s", result.read())
    plus_ones = json.loads(result.content)
    #logging.debug("%s %s %s %s", plus_ones['title'], plus_ones['title'], plus_ones['title'], plus_ones['title'] )

def getVimeoLikes(user):
    url = 'http://vimeo.com/api/v2/%s/likes.json' % user
    result = getUrl(url)
    if not result:
        return []

    media = []
    video_data = []
    likes_json = []
    try:
        likes_json = json.loads(result.content)
    except Exception, e:
        logging.error( "Error: %s", e )
        return []
    
    for vid in likes_json:
        #if vid['embed_privacy'].lower() != 'anywhere':
        #    continue
        
        media = [{
            'type': 'video',
            'html': '<iframe src="http://player.vimeo.com/video/%s" width="640" height="385" frameborder="0"></iframe>' % vid['id'],
            'display_url': vid['url'],
            'service_url': vid['url'],
            'thumbnail_url': vid['thumbnail_large'],
            'provider_name': 'Vimeo',
            'provider_url': 'htttp://vimeo.com'
            }]
        
        video_data.append({
            'service': 'vimeo',
            'title': vid['title'],
            'user_name': vid['user_name'],
            'user_url': vid['user_url'],            
            'screen_name': vid['user_name'],
            'media': media,
            'urls': [],
            'share_action': "rated",
            'created_at': vid['upload_date']                  
            })
    return video_data
    
def getTwitterFavorites(user):
    
    url = 'http://api.twitter.com/1/favorites.json?id=%s&include_entities=1&count=20' % user
    result = getUrl(url)
    if not result:
        return []

    favs_json = []
    try:
        favs_json = json.loads(result.content)
    except Exception, e:
        logging.error( "Error: %s", e )
        return []
    
    if 'error' in favs_json: return []
    
    twitter_favs = []
    favs = []
    urls = []
    for i, fav in enumerate(favs_json):

        entities = fav['entities']
        # get photos 
        media = []
        if 'media' in entities:
            for m in entities['media']:
                if m['type'].lower() != 'photo':
                    logging.debug('!!!!!!!!!!!!!!!!!!! type = %s', m['type'])
                    continue
                media.append({
                    'type': 'photo',
                    'display_url': m['display_url'],
                    'service_url': m['expanded_url'],
                    'thumbnail_url': m['media_url'],
                    'provider_name': m['display_url'],
                    'provider_url': m['display_url']
                    })


        twitter_fav = {
            'service': 'twitter',
            'title': fav['text'],
            'user_url': "http://twitter.com/" + fav['user']['screen_name'],     
            'user_name': fav['user']['name'],
            'screen_name': "@" + fav['user']['screen_name'],
            'media': media,
            'urls': [],
            'share_action': 'favorited',
            'created_at': fav['created_at']                  
            }
        twitter_favs.append(twitter_fav)

        # get urls and pack them in a list so we can call OEmbed client and fetch in parallel
        # save the index of the fav so we can attach the thumbnail we find
        if 'urls' in entities and len(entities['urls']) > 0:
            urls.append((entities['urls'][0], i))

        
    # Call OEmbed Client and get embeds for urls
    raw_urls = [u[0]['expanded_url'] for u in urls]
    logging.debug("[][][][][][][][]%s", raw_urls)
    oembed_responses = oEmbedClient.getEmbedContent(raw_urls)

    # look for images
    for i, oembed_response in enumerate(oembed_responses):
        media = []
        logging.debug("\n\n")

        if oembed_response == None: continue
        logging.debug("................................ %s", oembed_response)

        logging.debug("&&&&&&&&&&&& TYPE %s", oembed_response['type'])
        #logging.debug("&&&&&&&&&&&& EMBED URL %s", oembed_response.url)                                

        if oembed_response['type'] == "photo":
            logging.debug("&&&&&&&&&&&& EMBED URL %s", oembed_response['url'])
            media.append({
                'type': 'photo',
                'title': oembed_response.get('title'),
                'display_url': oembed_response['url'],
                'service_url': oembed_response['url'],
                'thumbnail_url': oembed_response['url'],
                'provider_name': oembed_response['provider_name'],
                'provider_url': oembed_response['provider_url']
                })
        if oembed_response['type'] == "video":
            logging.debug("&&&&&&&&&&&& THUMBNAIL HTML %s", oembed_response['html'])

            media.append({
                'type': 'video',
                'title': oembed_response['title'],
                'display_url': oembed_response['thumbnail_url'],
                'service_url': oembed_response['thumbnail_url'],
                'thumbnail_url': oembed_response['thumbnail_url'],
                'html': oembed_response['html'],
                'provider_name': oembed_response['provider_name'],
                'provider_url': oembed_response['provider_url']
                })
        if oembed_response['type'] == "rich":
            logging.debug("&&&&&&&&&&&& HTML %s", oembed_response['html'])                                

            media.append({
                'type': 'html',
                'html': oembed_response['html'],
                'title': oembed_response['title'],
                'display_url': oembed_response['thumbnail_url'],
                'service_url': oembed_response['thumbnail_url'],
                'thumbnail_url': oembed_response['thumbnail_url'],
                'provider_name': oembed_response['provider_name'],
                'provider_url': oembed_response['provider_url']
                })
        fav_index = urls[i][1]
        twitter_favs[fav_index]['media'] += media
                    
    return twitter_favs
    #logging.debug("%s %s %s %s", plus_ones['title'], plus_ones['title'], plus_ones['title'], plus_ones['title'] )

class UserHandle(db.Model):
    twitter_handle = db.StringProperty(multiline=False)
    youtube_handle = db.StringProperty(multiline=False)
    vimeo_handle = db.StringProperty(multiline=False)
    userhandle_name = db.StringProperty(multiline=False)
    
def userhandle_key(userhandle_name=None):
    return db.Key.from_path('UserHandle', userhandle_name or 'default_userhandle')

def validate_user_handles(request, response):
    twitter_handle = request.get('t')
    youtube_handle = request.get('yt')
    vimeo_handle = request.get('v')
    logging.debug("------------->twitter: %s youtube: %s vimeo: %s", twitter_handle, youtube_handle, vimeo_handle)  
    if len(twitter_handle) == 0 and len(youtube_handle) == 0 and len(vimeo_handle) == 0:
        response.set_status(400)
        response.out.write( "You must enter at least 1 username" )
        return False
    
    pv = formschema.SearchSchema()                
    try:
        #ne = formencode.validators.NotEmpty()
        pv.to_python({"twitter_handle": twitter_handle,
                      'youtube_handle': youtube_handle,
                      'vimeo_handle': vimeo_handle})
        
    except formencode.Invalid , msg:
        response.set_status(400)
        response.out.write( str(msg).capitalize().replace("_", " ") )
        return False

    return True

def validate_userhandle_name(request, response):
    userhandle_name = request.get('name')
    try:
        formencode.validators.PlainText(not_empty=True, strip=True).to_python(userhandle_name)
    except formencode.Invalid , msg:
        response.set_status(400)
        response.out.write( str(msg).capitalize().replace("_", " ") )
        return False
    
    return True

class PageHandler(webapp.RequestHandler):
    def get(self):
                    
        if not validate_userhandle_name(self.request, self.response):
            return        
        userhandle_name = self.request.get('name')        
        
        userhandle = db.GqlQuery("SELECT * "
                                 "FROM UserHandle "
                                 "WHERE ANCESTOR IS :1 ",
                                 userhandle_key(userhandle_name)).get()

        if not userhandle:
            self.response.set_status(403)
            self.response.out.write( "Page does not exist" )
            return
        
        #for userhandle in userhandles:            
        logging.debug("%s", userhandle)

        data = {
            'twitter_handle_default': userhandle.twitter_handle,
            'youtube_handle_default': userhandle.youtube_handle,
            'vimeo_handle_default': userhandle.vimeo_handle                
            }
        makoLookupDir = TemplateLookup(directories=['.'])
        mytemplate = Template(filename="index.html", lookup=makoLookupDir)
        self.response.out.write( mytemplate.render( **data ) )
                     
    def post(self):
        logging.debug("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ %s %s ", self.request, self.request.get('t'))
        
        if not validate_user_handles(self.request, self.response):
            return
        twitter_handle = self.request.get('t')
        youtube_handle = self.request.get('yt')
        vimeo_handle = self.request.get('v')              
          
        if not validate_userhandle_name(self.request, self.response):
            return        
        userhandle_name = self.request.get('name')

        userhandle = db.GqlQuery("SELECT * "
                                 "FROM UserHandle "
                                 "WHERE ANCESTOR IS :1 ",
                                 userhandle_key(userhandle_name)).get()

        if userhandle:
            self.response.set_status(200)
            self.response.out.write( "Name is already taken" )
            return
        
        logging.debug("------------->userhandle_name: %s", userhandle_name)        
        
        uh = UserHandle(parent = userhandle_key(userhandle_name))
        uh.userhandle_name = userhandle_name
        uh.twitter_handle = twitter_handle
        uh.youtube_handle = youtube_handle
        uh.vimeo_handle = vimeo_handle
        
        uh.put()

        self.response.set_status(200)
        #self.response.out.write( {"status": "OK"} )
        #self.redirect('/?' + urllib.urlencode({'userhandle_name': userhandle_name}))
        
    
class SearchHandler(webapp.RequestHandler):
   
    def get(self):
            
        if not validate_user_handles(self.request, self.response):
            return

        twitter_handle = self.request.get('t')
        youtube_handle = self.request.get('yt')
        vimeo_handle = self.request.get('v')
    
        logging.debug("------------->twitter: %s youtube: %s vimeo: %s", twitter_handle, youtube_handle, vimeo_handle)        

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            #getGooglePlusOnes()
            
            youtube_events = getYouTubeEvents(youtube_handle)            
            twitter_favorites = getTwitterFavorites(twitter_handle)
            vimeo_likes = getVimeoLikes(vimeo_handle)
            data = youtube_events + twitter_favorites + vimeo_likes

            self.response.set_status(200)        
            self.response.out.write( json.dumps(data) )
        else:
            data = {
                'twitter_handle_default': twitter_handle,
                'youtube_handle_default': youtube_handle,
                'vimeo_handle_default': vimeo_handle                
                }
            makoLookupDir = TemplateLookup(directories=['.'])
            mytemplate = Template(filename="index.html", lookup=makoLookupDir)
            self.response.out.write( mytemplate.render( **data ) )


class MainHandler(webapp.RequestHandler):
    def get(self):
        data = {
            'twitter_handle_default': '',
            'youtube_handle_default': '',
            'vimeo_handle_default': ''
            }
        makoLookupDir = TemplateLookup(directories=['.'])
        mytemplate = Template(filename="index.html", lookup=makoLookupDir)
        self.response.out.write( mytemplate.render( **data ) )
        
application = webapp.WSGIApplication([('/', MainHandler),
                                      ('/search', SearchHandler),
                                      ('/page', PageHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
