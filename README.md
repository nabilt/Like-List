LikeList
==========================================

* Author:    Nabil Tewolde (<nabil.tewolde@gmail.com>)
* Version:   0.1
* Website:   <http://www.likelist.ca>
* GitHub:    <https://github.com/nabilt/LikeList>

Like List create a personal page with your likes and favorites from across the web. You can think of it like about.me except with your 'likes' from various social networks embedded on a Pinterest style page.

Planned Improvements
--------------------

Infinite scroll, more services, pop out images for a larger view, user thumbnails, personal pages, visuals for tweets with no links and instructions :)

Unfortunately, Facebook doesn't provide a users likes without authentication, which defeats the purpose of having a public like list and Google Plus doesn't have an API for retrieving +1's yet.

Screenshots
-----------

![Screen shot 1](/nabilt/LikeList/raw/master/screenshot)

Installation
------------

Signup for a Google App Engine account and install the SDK <http://code.google.com/appengine/>.


Getting Started
---------------

Change the application name to the one you created in App Engine and update app.yaml

To get Google API keys go to <http://code.google.com/apis/console>

Checkout the [Bootstrap docs] on how to compile the less files. To get started style.css has been precompiled and contains all of the css including bootstrap and custom styles.

[Bootstrap docs]: http://twitter.github.com/bootstrap/less.html#compiling

If you decide to use embed.ly to convert urls into embeddable content go to <http://embed.ly/> to get an API key.

Change the YouTube API Key main.py

    YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'
    
Change the Embed.ly API key in oembed_client.py:

    embedly = Embedly('YOUR_EMBEDLY_API_KEY')

Change the Google Analytics tracking code in base.html:

    ....
    _gaq.push(['_setAccount', 'YOUR_GOOGLE_ANALYTICS_API_HERE']);
    ....

Change the share button urls and html meta data in base.html.

To start the development server run:

    python2.5 `which dev_appserver.py` <Your App Name>

To upload run:

    appcfg.py update <Your App Name>

Deployment
----------

Nothing special here. Just come up with a unique brand name and design.

License
-------

Like List by Nabil Tewolde is licensed under the GPLv3 license.