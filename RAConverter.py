from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
from RAGen.Generator import generate_stack
from RAGen.CPTGenerator import generate as cpt
from re import findall


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def ra_to_xml(text: str):
    counter = 1
    split = findall("{(.*?)}", text)
    # print(split)
    state_dict = {}
    RA = Element("dra")

    states = SubElement(RA, "states")
    for state in split[0].split(","):
        s = SubElement(states, "state")
        id = SubElement(s, "id")
        id.text = state
        state_dict[state] = s

    for registers in findall("\((.*?)\)", split[2]):
        reg = registers.split(",")
        available = SubElement(state_dict[reg[0]], "available-registers")
        for i in range(1, len(reg)):
            r = SubElement(available, "register")
            r.text = reg[i]

    initial = SubElement(RA, "initial-state")
    initial.text = split[1]

    transitions = SubElement(RA, "transitions")
    for tran in findall("\((.*?)\)", split[3]):
        resplit = tran.split(",")
        t = SubElement(transitions, "transition")
        f = SubElement(t, "from")
        f.text = resplit[0]
        inp = SubElement(t, "input")
        # inp.text = "boop"
        # counter += 1
        op = SubElement(t, "op")
        if resplit[3] == "K":
            resplit[3] = "Read"
            # inp.text = "pop"
        elif resplit[3] == "L":
            resplit[3] = "LFresh"
            # inp.text = "push"
        elif resplit[3] == "G":
            resplit[3] = "GFresh"
            # inp.text = "g_push"
        else:
            raise ValueError
        op.text = resplit[3]
        register = SubElement(t, "register")
        register.text = resplit[2]
        inp.text = f"{resplit[1]}"
        to = SubElement(t, "to")
        to.text = resplit[4]

    return prettify(RA)

# ra = cpt(400)
# print(ra)
# ra = ra_to_xml(cpt(400))
# with open("out.xml", "w") as f:
#     for line in ra:
#         f.write(line)

