
# None filter:
# class r3zmqfilter():
#    def do(self, eventname, eventdata):
#         return eventname
#

# Doom-Button filter:


class r3zmqfilter():

    def do(self, eventname, eventdata):
        if eventname == "BoreDoomButtonPressEvent":
            return "Dooom! The button has been pressed! Propably someone is bored and in need of company! ;-)"

        #elif eventname == "TempSensorUpdate":
        #    return "Temperature changed to " + str(eventdata['Value'])

        elif eventname == "PresenceUpdate":
            if eventdata['Present']:
                return "Realraum now open! \o/"
            else:
                return "Realraum now closed ..."

        elif eventname == "BackdoorAjarUpdate":
            if eventdata['Shut']:
                return "Backdoor closed."
            else:
                return "Backdoor opened."

        return eventname + ": " + str(eventdata)
