# FIMrecorder

## Resources
[FIM](https://www.uni-muenster.de/PRIA/en/FIM/index.html)
[FIMTrack](https://www.uni-muenster.de/PRIA/en/FIM/download.shtml)
[FIMTrack source code](https://github.com/i-git/FIMTrack)
[FIMrecorder source code](https://github.com/fncnt/fimrecorder)

## Installation
See [`README.md`](https://github.com/fncnt/fimrecorder/blob/master/README.md) in the repository. 

## Usage
Basic workflow

### Overview
![overview_lens.png](res/overview_lens.png)

### Configuration
To adjust settings not visible in the UI, click the button with three spurs labelled "Settings". This will launch your favourite text editor allowing you to edit the main configuration.

#### `settings.json`
`settings.json` is the primary configuration file and can be edited using any text editor. It contains data (`"Parameters"`) relevant to  your measurement (see [Measurement Annotations](#measurement-annotations) for a detailed description).
More importantly, it contains a `"Settings"` section controlling the behaviour of the application.
The following options can be modified:

`Background Frames to average`
:    test 

`Configuration Directory`
:	test

`Default Camera Parameters`
: test

`Extract every n-th Frame`
: test

`Logging Configuration`
: test

`Single Image Format`
: test

`Snapshot Directory`
: test

`Video Codec`
: test

`Video Container Format`
: test

*FIMrecorder* will fall back to hard-coded defaults and create a new configuration file if you happen to delete it.

#### `*.pfs` Files

### Recording Workflow

#### Pre-Recording

##### Checking Setup
1. Adjusting field of view.
2. Adjust aperture.
3. Adjust focus. Use the magnifying feature by scrolling on the preview for more control.


##### Measurement Annotations

##### Applying Camera parameters

##### Real-Time Signal Modifications

#### Post-Recording

##### Locating Recorded Data

##### Extracting Frames from Video Files

## Troubleshooting
Feel free to open an issue on [github](https://github.com/fncnt/fimrecorder/issues/new).
### Logging

#### `loggingconf.json`
[See `logging.config`](https://docs.python.org/3.6/howto/logging-cookbook.html#an-example-dictionary-based-configuration)
