import logging.config
import os
import json

with open('settings.json') as tempf:
    tempdict = json.load(tempf)
    configdir = tempdict['Settings']['Configuration Directory']
    configfile = tempdict['Settings']['Logging Configuration']
    with open(os.path.join(configdir, configfile)) as f:
        logging.config.dictConfig(json.load(f))
logger = logging.getLogger(__name__)