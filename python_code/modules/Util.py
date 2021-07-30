from configparser import ConfigParser
from types import SimpleNamespace

def get_config_publisher():
    # Read the config.cfg file
    config = ConfigParser()
    config.read('config/config.cfg')
    
    # Build my config object
    my_env = SimpleNamespace()
    
    my_env.TIMEZONE = config['general_info']['timezone']
    my_env.PATH_FILE = config['general_info']['path_file']
    
    my_env.CLIENT_NAME = config['iot_core_info']['client_name']
    my_env.TOPIC = config['iot_core_info']['topic']
    my_env.BROKER_PATH = config['iot_core_info']['broker_path']
    my_env.ROOT_CA_PATH = config['iot_core_info']['root_ca_path']
    my_env.PRIVATE_KEY_PATH = config['iot_core_info']['private_key_path']
    my_env.CERTIFICATE_PATH = config['iot_core_info']['certificate_path']
    
    return my_env

def get_config_consumer():
    # Read the config.cfg file
    config = ConfigParser()
    config.read('config/config.cfg')
    
    # Build my config object
    my_env = SimpleNamespace()
    my_env.STREAM_NAME = config['stream']['stream_name']
    
    return my_env