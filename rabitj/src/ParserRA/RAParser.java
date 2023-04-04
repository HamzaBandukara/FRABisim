package ParserRA;

import DataStructures.RA;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;

public class RAParser {
    public static Map<String, String> parseXML(String filename, String letter, RA ra) throws Exception {
        Map<String, String> stateRenamed = new HashMap<>();
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document document = builder.parse(filename);
        Element root = document.getDocumentElement();
        Node states = root.getElementsByTagName("states").item(0);
        while(states.hasChildNodes()){
            Node current = states.getFirstChild();
            if(current.hasChildNodes()){
                current.removeChild(current.getFirstChild());
                String currentState = current.getFirstChild().getTextContent();
                stateRenamed.put(currentState, letter + stateRenamed.size());
                ra.s_map.put(stateRenamed.get(currentState), new HashSet<>());
                current.removeChild(current.getFirstChild());
                current.removeChild(current.getFirstChild());
                Node availableRegisters = current.getFirstChild();
                while(availableRegisters.hasChildNodes()){
                    Node child = availableRegisters.getFirstChild();
                    if(child.hasChildNodes()){
                        ra.s_map.get(stateRenamed.get(currentState)).add(Integer.parseInt(child.getFirstChild().getTextContent()));
                    }
                    availableRegisters.removeChild(child);
                }
            }
            states.removeChild(current);
        }
        Node transitions = root.getElementsByTagName("transitions").item(0);
        while(transitions.hasChildNodes()){
            Node current = transitions.getFirstChild();
            if(current.hasChildNodes()){
                current.removeChild(current.getFirstChild());
                String src = stateRenamed.get(current.getFirstChild().getTextContent());
                current.removeChild(current.getFirstChild());
                current.removeChild(current.getFirstChild());
                String tag = current.getFirstChild().getTextContent();
                current.removeChild(current.getFirstChild());
                current.removeChild(current.getFirstChild());
                String type = current.getFirstChild().getTextContent();
                switch (type) {
                    case "LFresh" -> type = "L";
                    case "GFresh" -> type = "G";
                    case "Read" -> type = "K";
                    default -> {
                    }
                }
                current.removeChild(current.getFirstChild());
                current.removeChild(current.getFirstChild());
                int register = Integer.parseInt(current.getFirstChild().getTextContent());
                current.removeChild(current.getFirstChild());
                current.removeChild(current.getFirstChild());
                String tgt = stateRenamed.get(current.getFirstChild().getTextContent());
                ra.AddTransition(src, tag, register, type, tgt);
            }
            transitions.removeChild(current);
        }
        return stateRenamed;
    }
}
