#!/usr/bin/env python

"""
Usage:
  slack_notify -c <channel> -m <message>
  slack_notify [options]

Options:
   -c <channel>  channel to send messages into
   -m <message>  message to send to the named channel
   -b <botname>  bots name to display [default: orcabot]
   -i <boticon>  icon to show for the bot [default: :dolphin:]
   -h --help     show help text


"""
from docopt import docopt
import os, logging, sys
from slackclient import SlackClient as sl

class SlackNotify(object):
    """
    Slack notify send messages.
    """
    def __init__(self):
        self.user = "user"
        self.icon = "icon"
        self.token = os.environ.get('SLACK_TOKEN')
        self.cpm = "chat.postMessage"

    def send_message(self, chan, message):
        """
        Send the message.
        """
        slapi = sl(self.token)
        try:
            slapi.api_call(
              self.cpm,
              channel=chan,
              text=message,
              icon_emoji=self.icon,
              username=self.user
              )
        except Exception as e:
            logging.exception("Send message failed: %s", e)
        else:
            logging.info("Message sent successfully.")

    @classmethod
    def check_token(cls):
        """
        Check that the API token exists as an environment variable
        """
        t_token = os.environ.get('SLACK_TOKEN')
        if not t_token:
            logging.error("Slack token not set,process will now terminate.")
            sys.exit(0)

    def customize_bot(self, bicon, bname):
        """
        Change bot icon and name
        """
        self.icon = bicon
        self.user = bname

    def run(self):
        """
        Execute the process call
        """
        arguments = docopt(__doc__)
        self.check_token()
        self.customize_bot(arguments['-i'], arguments['-b'])
        self.send_message(arguments['-c'], arguments['-m'])


if __name__ == "__main__":
    SlackNotify().run()

