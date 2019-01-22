# -*- coding: utf-8 -*-

# Resolving gettext as _ for module loading.
from gettext import gettext as _

SKILL_NAME = "Slackful"

WELCOME = _("Welcome to Slackful Utility!")
HELP = _("Say about to understand more regarding Slackful and its purpose.")
ABOUT = _("Slackful is an app aimed toward helping you manage your online status effectively and easily when working remotely.")
STOP = _("Okay, just remember, I am always watching.")
FALLBACK = _("Slackful cannot help with that. Please use one of the defined functions.")
GENERIC_REPROMPT = _("Can Slackful assist you?")

# Status intent
STATUS_ASK = _("What status would you like me to set?")

MY_API = {
    "slack_channel": "https://hooks.slack.com/services/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",
}
