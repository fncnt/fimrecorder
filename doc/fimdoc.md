# FIMrecorder {-}

# Resources
[^fim]: [`https://www.uni-muenster.de/PRIA/en/FIM/index.html`](https://www.uni-muenster.de/PRIA/en/FIM/index.html)
[^fimtrack]: [`https://www.uni-muenster.de/PRIA/en/FIM/download.shtml`](https://www.uni-muenster.de/PRIA/en/FIM/download.shtml)
[^fimtracksourcecode]: [`https://github.com/i-git/FIMTrack`](https://github.com/i-git/FIMTrack)
[^fimrecorder]: [`https://github.com/fncnt/fimrecorder`](https://github.com/fncnt/fimrecorder)

# Installation
See `README.md`[^readme].

[^readme]: [`https://github.com/fncnt/fimrecorder/blob/master/README.md#prerequisites`](https://github.com/fncnt/fimrecorder/blob/master/README.md#prerequisites)

# Usage
Basic workflow

## Supported Devices
Currently, only Basler USB3 vision cameras recording in `Mono8` format are supported and only the model `acA1920-40um` actually has been tested.

## Overview
![The main UI components of *FIMrecorder*](res/overview_lens.png)

(@load) Loads parameters ((@measurement) & (@camera)) from a previously saved `.json` file.
(@save) Saves parameters ((@measurement) & (@camera)) to a new `.json` file.
(@record) Starts recording for the in (@measurement) specified duration.
(@snapshot) Saves a snapshot to [`Snapshot Directory`](#settingsjson)
(@extract) Extracts frames as single images from a specified video file. (Required for FIMTrack)
(@settings) settings.
(@measurement) This tab houses information relevant to your experiment such as measurement duration, species or genotype.
(@camera) Parameters in this tab modify the image signal your camera is acquiring.
(@preview) Live preview of the acquired image signal.
(@lens) Zooms by scrolling with your mouse or trackpad.
(@progress) When recording or extracting, the progress is displayed here.
(@status) Some relevant status messages appear in this area.

## Configuration
To adjust settings not visible in the UI, click the button labelled *Settings* (@settings). This will launch your favourite text editor allowing you to edit the main configuration.

### `settings.json` {#settingsjson}
`settings.json` is the primary configuration file and can be edited using any text editor. It contains data (`"Parameters"`) relevant to  your measurement (see [Measurement Annotations](#measurement-annotations) for a detailed description).
More importantly, it contains a `"Settings"` section controlling the behaviour of the application.
The following options can be modified:

`Background Frames to average`:
 ~  Number of Frames that should be used to construct an averaged static background image for background subtraction.
 ~  This setting *is* available from the UI.
 ~  `default: 100`

`Configuration Directory`:
 ~  Path of the directory where additional configurations files should be stored.
 ~  `settings.json` is **not** stored here.
 ~  `default: "config"`
 
`Default Camera Parameters`:
 ~  `default: "FIM_NodeMap.pfs"`

`Extract every n-th Frame`:
 ~  This setting *is* available from the UI.
 ~  `default: 1`

`Logging Configuration`:
 ~  `default: "loggingconf.json"`

`Single Image Format`:
 ~  `supported: ".tif"`, `".tiff"`, `".png"`
 ~  `default: ".tif"`

`Snapshot Directory`:
 ~  `default: "snapshots"`

`Video Codec`:
 ~  `default: "XVID"`

`Video Container Format`:
 ~  `default: ".avi"`

*FIMrecorder* will fall back to hard-coded defaults and create a new configuration file if you happen to delete it.

### `.pfs` Files

In addition to `settings.json` there are `.pfs` files in your `Configuration Directory` for every camera model you've used in *FIMrecorder*. Those text files are being generated when you use a device for the first time with *FIMrecorder* and include all the parameters of the specific model.

Those files can be used to modify the resolution, offset and binning parameters of your device.
If in doubt, take a look at your `Default Camera Parameters` for a comparison.
It is recommended to not change other parameters other than those in these files unless you've read the documentation for your camera model provided by Basler.

## Recording Workflow

### Pre-Recording

#### Checking Setup
1. Adjusting field of view.
2. Adjust aperture.
3. Adjust focus. Use the magnifying feature by scrolling on the preview for more control.


#### Measurement Annotations

#### Applying Camera parameters

#### Real-Time Signal Modifications

### Post-Recording

#### Locating Recorded Data

#### Extracting Frames from Video Files

# Troubleshooting
Feel free to open an issue on [github](https://github.com/fncnt/fimrecorder/issues/new)[^newissue].

[^newissue]: [`https://github.com/fncnt/fimrecorder/issues/new`](https://github.com/fncnt/fimrecorder/issues/new)

## Logging

### `loggingconf.json`
[See `logging.config`](https://docs.python.org/3.6/howto/logging-cookbook.html#an-example-dictionary-based-configuration)[^loggingconfig].

[^loggingconfig]: [`https://docs.python.org/3.6/howto/logging-cookbook.html#an-example-dictionary-based-configuration`](https://docs.python.org/3.6/howto/logging-cookbook.html#an-example-dictionary-based-configuration)
