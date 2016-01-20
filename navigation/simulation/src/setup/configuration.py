import xml.etree.ElementTree as ET

class Configuration:
    @staticmethod
    def get(tagPath):
        filepath = '../setup/config.xml'
    
        elTags = tagPath.split('.')
        
        config = ET.parse(filepath)
        el = config.getroot()
        
        for elTag in elTags:
            el = el.find(elTag)
            
        el = el.text.strip()
            
        try:
            return int(el)
        except:
            return float(el)
    
    