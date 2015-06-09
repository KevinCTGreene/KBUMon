import configparser

config = configparser.RawConfigParser()
config.read(r'config\settings.cfg')
print config.get('Settings', "username")
