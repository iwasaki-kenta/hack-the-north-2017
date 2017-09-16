from configparser import ConfigParser

parser = ConfigParser()
parser.read('keys.ini')

def google_key():
    return parser.get('keys', 'google')

def indico_key():
    return parser.get('keys', 'indico')