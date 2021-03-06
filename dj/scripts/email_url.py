#!/usr/bin/python

# email_url.py
# emails the video URL to the presenters

import itertools
from pprint import pprint

from email_ab import email_ab

class email_url(email_ab):

    ready_state = 7

    subject_template = "[{{ep.show.name}}] Video up: {{ep.name}}"
    body_body = """
The video is posted:
    {% for url in urls %} {{url}}
    {% endfor %}
Look at it, make sure the title is spelled right and the audio sounds reasonable.
If you are satisfied, tweet it, blog it, whatever it.  No point in making videos if no one watches them.

To approve it click the Approve button at
   {{ep.approve_url}}

As soon as you or someone approves your video, it will be tweeted on @NextDayVideo{% if ep.show.client.tweet_prefix %} tagged {{ep.show.client.tweet_prefix}}{% endif %}.  It will also be sent to the event organizers in hopes that they add it to the event website.
    {% if ep.twitter_url %}
It has been tweeted: {{ ep.twitter_url }}
Re-tweet it, blog it, whatever it.  No point in making videos if no one watches them.
    {% endif %}
    """


    def context(self, ep):
        ctx = super(email_url, self).context(ep)

        # dig around for URLs that might be relevant
        urls = filter( None,
                [ep.public_url,
                    ep.host_url,
                    ep.archive_ogv_url,
                    ep.archive_mp4_url] )

        ctx['urls'] = urls
        ctx['py_name'] = "email_url.py"

        return ctx


if __name__ == '__main__':
    p=email_url()
    p.main()

