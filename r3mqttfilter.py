#!/usr/bin/python
# -*- coding: utf-8 -*-


class r3mqttfilter():
    """
    List of all topics available in r3:
    https://realraum.at/wiki/doku.php?id=roomauto:mqtt_topics
    """

    # static:
    subscriptions = [
        ("realraum/+/boredoombuttonpressed", 1),
        # ("realraum/pillar/illumination", 1),
        ("realraum/olgafreezer/overtemp", 1),
        ("realraum/olgafreezer/sensorlost", 1),
        ("realraum/backdoorcx/gasalert", 1),
        # ("realraum/backdoorcx/powerloss", 1)
    ]

    def __init__(self):
        print '[r3mqtt] starting r3mqttfilter with', r3mqttfilter.subscriptions

    def do(self, eventname, eventdata):
        eventname = eventname.strip()
        print '[r3mqtt] received', eventname

        if eventname.endswith("/boredoombuttonpressed"):
            return "Dooom! The button has been pressed! Propably someone is bored and in need of company! ;-)"

        elif eventname.endswith("/olgafreezer/overtemp"):
            return "OLGA-Freezer overtemp!"

        elif eventname.endswith("/olgafreezer/sensorlost"):
            return "OLGA-Freezer sensorlost!"

        elif eventname.endswith("/gasalert"):
            return "LPG/Gas-Alert on CX-Ceiling is triggered ..."

        elif eventname.endswith("/powerloss"):
            return "UPS reports powerloss, power-regained or change in battery charge ..."

        # elif eventname.endswith("/temperature"):
        #    return "Temperature changed to " + str(eventdata['Value'])

        # elif eventname.endswith("/presence"):
        #    if eventdata['Present']:
        #        return "Realraum now open! \o/"
        #    else:
        #        return "Realraum now closed ..."

        # elif eventname.endswith("/backdoorcx/ajar"):
        #    if eventdata['Shut']:
        #        return "Backdoor closed."
        #    else:
        #        return "Backdoor opened."

        # return eventname + ": " + str(eventdata)

        return None
