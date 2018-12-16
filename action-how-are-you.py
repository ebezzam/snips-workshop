#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import ConfigParser
from hermes_python.hermes import Hermes
import pyowm
import io


CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

INTENT_HOW_ARE_YOU = "bezzam:how_are_you"
INTENT_GOOD = "bezzam:feeling_good"
INTENT_BAD = "bezzam:feeling_bad"
INTENT_ALRIGHT = "bezzam:feeling_alright"

INTENT_FILTER_FEELING = [INTENT_GOOD, INTENT_BAD, INTENT_ALRIGHT]


def main():
    config = read_configuration_file(CONFIG_INI)
    owm = pyowm.OWM(config["secret"]["owm_key"])

    with Hermes("localhost:1883") as h:
        h.owm = owm
        h.subscribe_intent(INTENT_HOW_ARE_YOU, how_are_you_callback) \
         .subscribe_intent(INTENT_GOOD, feeling_good_callback) \
         .subscribe_intent(INTENT_BAD, feeling_bad_callback) \
         .subscribe_intent(INTENT_ALRIGHT, feeling_alright_callback) \
         .start()


def how_are_you_callback(hermes, intent_message):
    session_id = intent_message.session_id

    # set mood according to weather
    config = read_configuration_file(CONFIG_INI)
    observation = hermes.owm.weather_at_place(config["secret"]["city"])
    w = observation.get_weather()
    temp = w.get_temperature('celsius')["temp"]
    if temp >= float(config["secret"]["temperature_threshold"]):
        response = "I'm feeling great! "
    else:
        response = "Not so good. "
    response += "It's {} degrees in {}. How are you?".format(temp, config["secret"]["city"])

    hermes.publish_continue_session(session_id, response, INTENT_FILTER_FEELING)


def feeling_good_callback(hermes, intent_message):
    session_id = intent_message.session_id
    response = "That's awesome! I'm happy to hear that."
    hermes.publish_end_session(session_id, response)


def feeling_bad_callback(hermes, intent_message):
    session_id = intent_message.session_id
    response = "Sorry to hear that. I hope you feel better soon."
    hermes.publish_end_session(session_id, response)


def feeling_alright_callback(hermes, intent_message):
    session_id = intent_message.session_id
    response = "That's cool."
    hermes.publish_end_session(session_id, response)


class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()


if __name__ == "__main__":
    main()
