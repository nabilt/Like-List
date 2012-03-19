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

# modified from the oohembed project
# http://code.google.com/p/oohembed/source/browse/app/provider/endpoints.json?r=4b666a08fbe2329e7f9c34b97bad32a04a098dcb
OEMBED_ENDPOINTS = [
    {
        "url": "http://*blip.tv/*", 
        "url_re": "blip\\.tv/.+", 
        "example_url": "http://pycon.blip.tv/file/2058801/", 
        "endpoint_url": "http://blip.tv/oembed/", 
        "title": "blip.tv",
        "url_params": {"maxwidth": "960"}

        }, 
    {
        "url": "(http://*dailymotion.com/*|http://*dai.ly/*)", 
        "url_re": "dailymotion\\.com/.+", 
        "example_url": "http://www.dailymotion.com/video/x5ioet_phoenix-mars-lander_tech", 
        "endpoint_url": "http://www.dailymotion.com/api/oembed/", 
        "title": "Dailymotion"
        }, 
    {
        "url": "(http://*flickr.com/*|http://flic.kr/*)", 
        "url_re": "flickr\\.com/.+", 
        "example_url": "http://www.flickr.com/photos/fuffer2005/2435339994/", 
        "endpoint_url": "http://www.flickr.com/services/oembed/", 
        "title": "Flickr Photos"
        }, 
    {
        "url": "(http://*hulu.com/*|http://*hulu.tv/*)", 
        "url_re": "hulu\\.com/.+", 
        "example_url": "http://www.hulu.com/watch/20807/late-night-with-conan", 
        "endpoint_url": "http://www.hulu.com/api/oembed.json", 
        "title": "Hulu"
        }, 
    {
        "url": "http://*nfb.ca/film/*", 
        "url_re": "nfb\\.ca/film/[-\\w]+/?", 
        "example_url": "http://www.nfb.ca/film/blackfly/", 
        "endpoint_url": "http://www.nfb.ca/remote/services/oembed/", 
        "title": "National Film Board of Canada"
        }, 
    {
        "url": "http://qik.com/video/*", 
        "url_re": "qik\\.com/.+", 
        "example_url": "http://qik.com/video/86776", 
        "endpoint_url": "http://qik.com/api/oembed.json", 
        "title": "Qik Video"
        }, 
    {
        "url": "http://*revision3.com/*", 
        "url_re": "revision3\\.com/.+", 
        "example_url": "http://www.revision3.com/diggnation/2008-04-17xsanned/", 
        "endpoint_url": "http://www.revision3.com/api/oembed/", 
        "title": "Revision3"
        }, 
    {
        "url": "http://*scribd.com/*", 
        "url_re": "scribd\\.com/.+", 
        "example_url": "http://www.scribd.com/doc/17896323/Indian-Automobile-industryPEST", 
        "endpoint_url": "http://www.scribd.com/services/oembed", 
        "title": "Scribd"
        }, 
    {
        "url": "http://*viddler.com/explore/*", 
        "url_re": "viddler\\.com/explore/.*/videos/\\w+/?", 
        "example_url": "http://www.viddler.com/explore/engadget/videos/14/", 
        "endpoint_url": "http://lab.viddler.com/services/oembed/", 
        "title": "Viddler Video"
        }, 
    {
        "url": ["http://*vimeo.com/*", "http://*vimeo.com/groups/*/videos/*"], 
        "url_re": "vimeo\\.com/.*", 
        "example_url": "http://www.vimeo.com/1211060", 
        "endpoint_url": "http://www.vimeo.com/api/oembed.json", 
        "title": "Vimeo"
        }, 
    {
        "url": "(http://*youtube.com/*|http://youtu.be/*)", 
        "url_re": "youtube\\.com/watch.+v=[\\w-]+&?", 
        "example_url": "http://www.youtube.com/watch?v=vk1HvP7NO5w", 
        "endpoint_url": "http://www.youtube.com/oembed", 
        "title": "YouTube"
        },
    {
        "url": "http://dotsub.com/view/*", 
        "url_re": "dotsub\\.com/view/[-\\da-zA-Z]+$",
        "example_url": "http://dotsub.com/view/10e3cb5e-96c7-4cfb-bcea-8ab11e04e090", 
        "endpoint_url": "http://dotsub.com/services/oembed", 
        "title": "dotSUB.com"
        },
    {
        "url": "http://yfrog.(com|ru|com.tr|it|fr|co.il|co.uk|com.pl|pl|eu|us)/*", 
        "url_re": "yfrog\\.(com|ru|com\\.tr|it|fr|co\\.il|co\\.uk|com\\.pl|pl|eu|us)/[a-zA-Z0-9]+$",
        "example_url": "http://yfrog.com/0wgvcpj", 
        "endpoint_url": "http://www.yfrog.com/api/oembed", 
        "title": "YFrog"
        },
    {
        "url": "http://*clikthrough.com/theater/video/*", 
        "url_re": "clikthrough\\.com/theater/video/\\d+$",
        "example_url": "http://www.clikthrough.com/theater/video/55", 
        "endpoint_url": "http://clikthrough.com/services/oembed", 
        "title": "Clikthrough"
        },
    {
        "url": "http://*kinomap.com/*", 
        "url_re": "kinomap\\.com/.+",
        "example_url": "http://www.kinomap.com/kms-vzkpc7", 
        "endpoint_url": "http://www.kinomap.com/oembed", 
        "title": "Kinomap"
        },
    {
        "url": ["http://*photobucket.com/albums/*", "http://*photobucket.com/groups/*"], 
        "url_re": "photobucket\\.com/(albums|groups)/.+$",
        "example_url": "http://img.photobucket.com/albums/v211/JAV123/Michael%20Holland%20Candle%20Burning/_MG_5661.jpg", 
        "endpoint_url": "http://photobucket.com/oembed", 
        "title": "Photobucket"
        },    
    {
        "url": "http://*collegehumor.com/video/*", 
        "url_re": "collegehumor\\.com/.+",
        "example_url": "http://www.collegehumor.com/video/3922232/prank-war-7-the-half-million-dollar-shot", 
        "endpoint_url": "http://www.collegehumor.com/oembed.json", 
        "title": "College Humor"
        },
    {
        "url": "(http://*polldaddy.com/*|http://*poll.fm/*)", 
        "url_re": "polldaddy\\.com/.+",
        "example_url": "http://www.polldaddy.com/poll/6001531/", 
        "endpoint_url": "http://www.polldaddy.com/oembed/", 
        "title": "Poll Daddy"
        },
    {
        "url": "http://*ifixit.com/*", 
        "url_re": "ifixit\\.com/.+",
        "example_url": "http://www.ifixit.com/Teardown/iPhone-4-Teardown/3130/1", 
        "endpoint_url": "http://www.ifixit.com/Embed", 
        "title": "iFixit"
        },
    {
        "url": "http://*smugmug.com/*", 
        "url_re": "smugmug\\.com/.+",
        "example_url": "http://www.smugmug.com/popular/today/1735027394_RRwv7sK#!i=1735027394&k=RRwv7sK", 
        "endpoint_url": "http://api.smugmug.com/services/oembed/", 
        "title": "SmugMug"
        },
    {
        "url": "http://*slideshare.net/*", 
        "url_re": "slideshare\\.com/.+",
        "example_url": "http://www.slideshare.net/haraldf/business-quotes-for-2011", 
        "endpoint_url": "http://www.slideshare.net/api/oembed/2", 
        "title": "SlideShare"
        },
    {
        "url": "http://*wordpress.com/*", 
        "url_re": "wordpress\\.com/.+",
        "example_url": "http://en.blog.wordpress.com/2012/02/14/new-theme-retro-fitted/", 
        "endpoint_url": "http://public-api.wordpress.com/oembed/", 
        "title": "Wordpress",
        "url_params": {"for": "likeification.appspot.com"}
        },
    {
        "url": "http://*5min.com/video/*", 
        "url_re": "5min\\.com/.+",
        "example_url": "http://www.5min.com/Video/How-to-Make-a-Chocolate-Cake-6872", 
        "endpoint_url": "http://api.5min.com/oembed.json", 
        "title": "5min",
        },
    {
        "url": "http://*funnyordie.com/*", 
        "url_re": "funnyordie\\.com/.+",
        "example_url": "http://www.funnyordie.com/videos/24acf5ae41/eastbound-downton", 
        "endpoint_url": "http://www.funnyordie.com/oembed", 
        "title": "Funny Or Die",
        },
    {
        "url": "http://*justin.tv/*", 
        "url_re": "justin\\.tv/.+",
        "example_url": "http://www.justin.tv/twit", 
        "endpoint_url": "http://api.justin.tv/api/embed/from_url.json", 
        "title": "Justin",
        },
    {
        "url": "http://*bambuser.com/*", 
        "url_re": "bambuser\\.com/.+",
        "example_url": "http://bambuser.com/v/2083252", 
        "endpoint_url": "http://api.bambuser.com/oembed.json", 
        "title": "bambuser",
        },
    {
        "url": "http://my.opera.com/*", 
        "url_re": "my\\.opera\\.com/.+",
        "example_url": "http://my.opera.com/susiM/albums/show.dml?id=3080571", 
        "endpoint_url": "http://my.opera.com/service/oembed", 
        "title": "My Opera",
        },
    {
        "url": "(http://*ustream.tv/*|http://ustre.am/*)", 
        "url_re": "ustream\\.tv/.+",
        "example_url": "http://www.ustream.tv/channel/adafruit-industries", 
        "endpoint_url": "http://www.ustream.tv/oembed", 
        "title": "Ustream",
        },
    ]

"""
{
"url": "", 
"url_re": "\\.com/.+",
"example_url": "", 
"endpoint_url": "", 
"title": "",
}
"""
