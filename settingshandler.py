import json
import os
import errno
from datetime import timezone, datetime
# Handles loading and saving of settings and parameters related to measurements and UI
# Parameters of Basler Ace cameras are dealt with in pyloncom.py
#

class SettingsHandler:

    # define parameters here
    def __init__(self):
        # hard-coded so we still can restore default parameters if somebody deleted the file
        self.parameters = {'Recording Duration': "00:05:00.0",
                           'Frame Rate': 41.58177,
                           'Exposure Time': 20000,
                           'User Data': {'Species': "",
                                         'Strain': "",
                                         'Genotype': "",
                                         'More Info': ""
                                         }
                           }

        self.settings = {'Snapshot Directory': "snapshots",
                         'Recording Directory': "FIMrecordings",
                         'Configuration Directory': "config",
                         'Default Camera Parameters': "FIM_NodeMap.pfs",
                         'Video Codec': 'XVID'
                         }
        # load settings file on init or create a new one if there is no present
        try:
            self.loadSettings()
            self.createDir(self.settings['Snapshot Directory'])
            self.createDir(self.settings['Recording Directory'])
            self.createDir(self.settings['Configuration Directory'])
        except Exception as e:
            print(str(e))
            print("Creating new settings.json file")
            self.saveSettings()

    def createDir(self, path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    # call on exit of application
    # or when deemed necessary (e.g. when finishing a recording)
    # nonmeasurement=True saves application-specific parameters
    # such as default file paths
    def saveSettings(self, fpath="", fname="settings.json", onlyparameters=False):
        # We don't want the user to specify the date.
        self.parameters['Date'] = str(datetime.now(timezone.utc).astimezone())
        try:
            file = open(os.path.join(fpath, fname), 'w')
            #dumpling = None
            if onlyparameters:
                dumpling = dict(Parameters=self.parameters)
            else:
                dumpling = dict(Settings=self.settings, Parameters=self.parameters)
            json.dump(dumpling, file, sort_keys=True, indent=4)
        except Exception as e:
            print(str(e))
        finally:
            file.close()
        return 0

    # call on startup of application
    # or manually to reproduce measurements
    # see https://www.python.org/dev/peps/pep-0448/ for merging dicts
    # This way incomplete json files cause no problems
    def loadSettings(self, fpath="", fname="settings.json", onlyparameters=False):
        try:
            file = open(os.path.join(fpath, fname), 'r')
            dumpling = json.load(file)
            if not onlyparameters:
                try:
                    self.settings = {**self.settings, **dumpling['Settings']}
                except Exception as e:
                    print("There is no key ", str(e), ".")
            self.parameters = {**self.parameters, **dumpling['Parameters']}

        except Exception as e:
            print(str(e))
        finally:
            file.close()
        return 0

    def __str__(self):
        return json.dumps(self.parameters, sort_keys=True, indent=4)
