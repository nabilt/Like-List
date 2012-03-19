import formencode

class SearchSchema(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    vimeo_handle = formencode.validators.PlainText(max=100, strip=True)
    twitter_handle = formencode.validators.PlainText(max=100, strip=True)
    youtube_handle = formencode.validators.PlainText(max=100, strip=True)
