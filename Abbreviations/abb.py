'''
Extends the abbreviations
Example string to be changed: 
    Ramp  to I-90/I-94 Westbound and W Monroe St - Roadwork.

abbreviations:
    St = Street
    Rd = Road
    Ave = Avenue
    Expy = Expressway
    Blvd = Boulevard
    Dr = Drive
'''

def abbrev(abbreviation):
    if " Rd " in abbreviation:
        return abbreviation.replace(" Rd ", " Road ")
    elif " St " in abbreviation:
        return abbreviation.replace(" St ", " Street ")
    elif " Ave " in abbreviation:
        return abbreviation.replace(" Ave ", " Avenue ")
    elif " Expy " in abbreviation:
        return abbreviation.replace(" Expy ", " Expressway ")
    elif " Blvd " in abbreviation:
        return abbreviation.replace(" Blvd ", " Boulevard ")
    elif " Dr " in abbreviation:
        return abbreviation.replace(" Dr ", " Drive ")
    elif "/" in abbreviation:
        return abbreviation.replace("/", " and ")
    else:
        return abbreviation