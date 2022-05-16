# Reads in the XML examples in the desired format
import xml.etree.ElementTree as ET
import os

def parseXML(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    stateset = set()
    availabilityset = {}
    initialstate = ""
    registerset = set()
    transitionset = set()
    finalstate = ""
    for item in root.findall('./states'):
        for state in item.findall('./state'):
            for id in state.findall('./id'):
                curr_id = str(id.text.encode('utf8'))
                curr_id = curr_id[2:-1]
                curr_state = curr_id
                stateset.add(curr_id)
                availabilityset[curr_state] = set()
                for registers in state.findall('./available-registers'):
                    for register in registers.findall('./register'):
                        curr_id = str(register.text.encode('utf8'))
                        curr_id = curr_id[2:-1]
                        availabilityset[curr_state].add(curr_id)
                        curr_id = "(" + curr_id + ",#)"
                        registerset.add(curr_id)
    for item in root.findall('initial-state'):
        curr_id = str(item.text.encode('utf8'))
        curr_id = curr_id[2:-1]
        initialstate = curr_id
    for item in root.findall('./transitions'):
        for transition in item.findall('./transition'):
            source = ""
            tag = ""
            label = ""
            target = ""
            for id in transition.findall('./from'):
                curr_id = str(id.text.encode('utf8'))
                curr_id = curr_id[2:-1]
                source = curr_id
            for id in transition.findall('./op'):
                curr_id = str(id.text.encode('utf8'))
                curr_id = curr_id[2:-1]
                if curr_id == "GFresh":
                    curr_id = "G"
                elif curr_id == "LFresh":
                    curr_id = "L"
                else:
                    curr_id = "K"
                label = curr_id
            for id in transition.findall('./input'):
                curr_id = str(id.text.encode('utf8'))
                curr_id = curr_id[2:-1]
                tag = curr_id
            for id in transition.findall('./register'):
                curr_id = str(id.text.encode('utf8'))
                curr_id = curr_id[2:-1]
                label = curr_id + "," + label
            for id in transition.findall('./to'):
                curr_id = str(id.text.encode('utf8'))
                curr_id = curr_id[2:-1]
                target = curr_id
            transitionset.add((source,tag,label,target))
    ret = ""
    for key in availabilityset:
        ret += "({}".format(key)
        for val in availabilityset[key]:
            ret += ", {}".format(val)
        ret += ")"
    ret = str(stateset) + "{" + initialstate + "}{" + ret + "}" + str(transitionset) + "{}"
    ret = ret.replace("'", "")
    ret = ret.replace(" ", "")
    return ret

def main():
    for filename in os.listdir('./xml-inputs'):
        fra = parseXML('./xml-inputs/'+filename)
        writer = open('./xml-outputs/' + filename.split(".")[0], "w")
        # writer = open('./xml-outputs/DEQOnline' + str(counter), "w")
        writer.write(fra)
        writer.close()

if __name__ == "__main__":
    main()