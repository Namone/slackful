# -*- coding: utf-8 -*-

# Slackful: An Alexa skill that interacts witih Slack API

from ask_sdk_model.dialog import (
    ElicitSlotDirective, DelegateDirective)

from ask_sdk_model import (
    Response, IntentRequest, DialogState, SlotConfirmationStatus, Slot)

from ask_sdk_model.slu.entityresolution import StatusCode

import logging
import random
import gettext

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor)
from ask_sdk_core.utils import is_intent_name, is_request_type
from typing import Union, Dict, Any, List

from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

from alexa import slackful_data

# Skill Builder object
sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Request Handler classes
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        # logger.info(_("This is an untranslated message"))

        speech = _(slackful_data.WELCOME)
        speech += " " + _(slackful_data.HELP)
        handler_input.response_builder.speak(speech)
        handler_input.response_builder.ask(_(
            slackful_data.GENERIC_REPROMPT))
        return handler_input.response_builder.response

# StatusIntent handler
class StatusIntentHandler(AbstractExceptionHandler):
    """Handler for setting status via Slack API."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("StatusIntent")(handler_input)

    def handle(self, hanlder_input):
        # type: (HanlderInput) -> Response
        logger.info("Running StatusIntent...")

        slotValue = self['slots']['slackStatus']['value'];
        handler_input.response_builder.speak(_("You said " + slotValue))
        return handler_input.response_builder.response

# AboutIntent handler
class AboutIntentHandler(AbstractRequestHandler):
    """Handler for about intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AboutIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In AboutIntent...")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(slackful_data.ABOUT))
        return handler_input.response_builder.response

# Exception Handler classes
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch All Exception handler.
    This handler catches all kinds of exceptions and prints
    the stack trace on AWS Cloudwatch with the request envelope."""
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        logger.info("Original request was {}".format(
            handler_input.request_envelope.request))

        speech = "Sorry, there was some problem. Please try again!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response

class LocalizationInterceptor(AbstractRequestInterceptor):
    """Add function to request attributes, that can load locale specific slackful_data."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))
        i18n = gettext.translation(
            'base', localedir='locales', languages=[locale], fallback=True)
        handler_input.attributes_manager.request_attributes[
            "_"] = i18n.gettext


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for skill session end."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
        logger.info("Session ended with reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for help intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(
            slackful_data.HELP)).ask(_(slackful_data.HELP))
        return handler_input.response_builder.response


class ExitIntentHandler(AbstractRequestHandler):
    """Single Handler for Cancel, Stop intents."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ExitIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(
            slackful_data.STOP)).set_should_end_session(True)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for handling fallback intent or Yes/No without
    restaurant info intent.
     2018-May-01: AMAZON.FallackIntent is only currently available in
     en-US locale. This handler will not be triggered except in that
     locale, so it can be safely deployed for any locale."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.FallbackIntent")(handler_input) or
                ("restaurant" not in session_attr and (
                    is_intent_name("AMAZON.YesIntent")(handler_input) or
                    is_intent_name("AMAZON.NoIntent")(handler_input))
                 ))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(
            slackful_data.FALLBACK).format(slackful_data.SKILL_NAME)).ask(_(
                slackful_data.FALLBACK).format(slackful_data.SKILL_NAME))

        return handler_input.response_builder.response


# Add all request handlers to the skill.
sb.add_request_handler(LaunchRequestHandler())

sb.add_request_handler(AboutIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Add exception handler to the skill.
sb.add_exception_handler(CatchAllExceptionHandler())

# Add locale interceptor to the skill.
sb.add_global_request_interceptor(LocalizationInterceptor())

# Expose the lambda handler to register in AWS Lambda.
lambda_handler = sb.lambda_handler()
