
# None filter:
# class r3mqttfilter():
#    def do(self, eventname, eventdata):
#         return eventname
#

# Doom-Button filter:


class r3mqttfilter():

    subscriptions = [("realraum/+/boredoombuttonpressed", 1)]

    def do(self, eventname, eventdata):
        eventname = eventname.strip()
        print '[r3mqtt] received', eventname
        if eventname.endswith("/boredoombuttonpressed"):
            return "Dooom! The button has been pressed! Propably someone is bored and in need of company! ;-)"

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
