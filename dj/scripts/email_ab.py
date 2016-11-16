#!/usr/bin/python

# email_ab.py
# abstract email class

from django.core.mail import get_connection, EmailMessage

from django.template import Context, Template

from process import process
from django.conf import settings

import random

class email_ab(process):

    def mk_body( self, ep, context):

        body_template = \
                self.body_header + self.body_body + self.body_footer 

        if not ep.emails:
            body_alert = """
Hello show organizer(s)!

This item does not have an email address, so it is getting sent to you.
Please review and forward it on to the presenter.

In case it isn't clear what this item is about, here is some context:
    name: {{ep.name}}
    authors: {{ep.authors}}
    released: {{ep.released}}
    conf_url: {{ep.conf_url}}
    conf_key: {{ep.conf_key}}
    room: {{ep.location}}
    start: {{ep.start}}

What follows is what was intended to be sent to the presenter:
"""
            body_template = body_alert + body_template\

        body = Template( 
                body_template
                ).render(Context(context, autoescape=False))

        return body

    subject_template = "stub testing:{{ep.name}}"

    body_header = """
Hi,

This is Veyepar, the automated video processing system.

    """
    body_body = "stub testing:{{ep.description}}"

    body_footer = """
Email generated by https://github.com/CarlFK/veyepar/blob/master/dj/scripts/{{py_name}}
but replies go to real people.

Reference: http://veyepar.nextdayvideo.com/main/E/{{ep.id}}/
"""
    py_name = "email_ab.py"

   
    def more_context(self, ep):
        # hook to specify more context
        # like png url
        return {}

    def process_ep(self, ep):

        # if there is no email, use the client's.
        # like for lightning talks.
        emails = ep.emails or ep.show.client.contacts

        if self.options.verbose: print(emails)

        if emails: 
            tos = [e.strip() for e in emails.split(',')]

            subject = Template(self.subject_template).render(
                    Context({'ep':ep}, autoescape=False))

            context = { 'ep':ep, 
                    'py_name':self.py_name, 
                    # 'MEDIA_URL':settings.MEDIA_URL,
                    }
            more_context = self.more_context(ep)
            for k in more_context:
                context[k] = more_context[k]
            
            body = self.mk_body(ep, context)

            # sender = 'Carl Karsten <carl@nextdayvideo.com>'
            sender = settings.EMAIL_SENDER
            ccs = [e.strip() for e in settings.EMAIL_CC.split(',')]
            # make a list of addresses:
            reply_tos = [sender,] + ccs + \
                    ep.show.client.contacts.split(',')
            # headers={Reply-To... needs to be a string of comma seperated 
            reply_to = ','.join( reply_tos )
            headers = {
                     'Reply-To': reply_to,
                    # 'Cc': cc,
                    # 'From': sender,
                        }    

            if self.options.test:
                print("tos:", tos)
                print("ccs:", ccs)
                print("subject:", subject)
                print("headers:", headers)
                print("context:", context)
                print("body:", body)
                ret = False
            else:

                email = EmailMessage(
                        subject, body, sender, tos, 
                        headers=headers, cc=ccs ) 
                connection = get_connection()
                ret = connection.send_messages([email])
                print(tos, ret)
                ret = True # need to figure out what .send_messages returns

        else:
            print("no emails!")
            ret = False

        return ret

if __name__ == '__main__':
    p=email_ab()
    p.main()

