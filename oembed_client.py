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

import oembed
from endpoints import OEMBED_ENDPOINTS
import urllib2
import urlparse
from google.appengine.api import urlfetch
import logging

from embedly.client import Embedly
from embedly.models import Url

embedly = Embedly('YOUR_EMBEDLY_API_KEY')

#http://hulu.tv/1Xw
URL_SHORTENERS = [
    'http://bit.ly',
    'http://goo.gl',
    'http://t.co',
    'http://tinyurl.com',
    'http://fb.me',
    'http://ow.ly',
    'http://y.ahoo.it',
    'http://share.yhoo.it',
    'http://wp.me',
    'http://flic.kr'
    ]

class OEmbedClient:
    def __init__(self):
        self.consumer = oembed.OEmbedConsumer()
        for endpoint in OEMBED_ENDPOINTS:

            url = endpoint['url']
            if type(url) == str:
                url = [url]

            endpoint = oembed.OEmbedEndpoint(endpoint['endpoint_url'], url)
            self.consumer.addEndpoint(endpoint)

    @classmethod
    def expandUrl(cls, url):
        hostname = 'http://' + urlparse.urlparse(url).hostname
        logging.debug("&&&&&&&&&&&& ^^^^^^^^ %s   %s", hostname, url)

        if hostname in URL_SHORTENERS:
            try:
                response = urllib2.urlopen(url) # Some shortened url
                logging.debug("-------------> EXPANDED %s ", response.url)
                return response.url
            except Exception ,e:
                logging.debug("!!!!!!!! TIMEOUT !!!!!!!! %s", e)
                return url
        return url
    
    def getEmbedContent(self, url):
        #"""
        try:
            objs = embedly.oembed(url, maxwidth=500)
            return objs
        except Exception, msg:
            logging.debug("%s", msg)
            return []
        #"""

        # Attempted to manualy do what embedly does by using OEmbed API that some
        # services provide. Turns out to be too slow doesn't work in enough cases.
        """
        if type(url) != list:
            url = [url]

        rpcs = []
        for u in url:
            rpc = urlfetch.create_rpc()
            urlfetch.make_fetch_call(rpc, u)
            rpcs.append( (rpc,u) )

        response = []
        for rpc in rpcs:
            result = rpc[0].get_result()
            url = rpc[1]
            
            url =  self.expandUrl(url)
                    
            try:            
                response.append(self.consumer.embed( url, "json"))
            except (oembed.OEmbedNoEndpoint, oembed.OEmbedError) ,e:
                logging.debug("%s", e)
            except Exception ,e:
                logging.debug("%s", e)
        
        return response
        """


# For testing                
if __name__ == "__main__":

    consumer = oembed.OEmbedConsumer()
    
    count = 0
    for endpoint in OEMBED_ENDPOINTS:

        url = endpoint['url']
        if type(url) == str:
            url = [url]

        print url
        endpoint = oembed.OEmbedEndpoint(endpoint['endpoint_url'], url)
        consumer.addEndpoint(endpoint)

    for endpoint in OEMBED_ENDPOINTS:
        try:
            #'http://www.flickr.com/photos/wizardbt/2584979382/'
            endpoint_url = endpoint['example_url']
            
            opts = {}
            if 'url_params' in endpoint:
                opts = endpoint['url_params']

            response = consumer.embed( endpoint_url, "json", **opts)
            print response['title']

            #import pprint
            #pprint.pprint(response.getData())
            print '\n'
        except (oembed.OEmbedNoEndpoint, oembed.OEmbedError) ,e:
            print e, '\n'
