# FIMRecorder

This program is
a simple recording application for FIM related
measurements. 
Currently only Basler USB3 vision cameras are supported.

## Documentation

You can find more detailed information in [`doc/fimdox.md`](https://github.com/fncnt/fimrecorder/blob/master/doc/fimdoc.md).

To create a `.pdf` file, simply run:
```
pandoc doc/fimdoc.md -t latex -o fimdoc.pdf --number-sections --toc
```

## Usage
There are two different options to use this application.
Both of them require nearly the same setup:

### Prerequisites

First, install [`python`](https://www.python.org/)
(due to the pypylon dependency, only versions 
up to Python 3.6 are currently supported).

Install the following packages using `pip`:
- `pypylon`
- `PyQT5`
- `opencv-python`
- `vispy`

Install the [Basler Pylon 5 Runtime](https://www.baslerweb.com/de/vertrieb-support/downloads/downloads-software/pylon-5-0-12-runtime/).

### Running from Source

Connect your USB3 vision Basler camera to a USB3 port
and start the application on the command line interface via
```
python fimrecorder.py
```
or
```
./fimrecorder.py
```

### Creating a portable executable file.
**This is currently only supported on Windows (64bit)!**

Install `pyinstaller` via `pip` and run
```
pyinstaller fimrecorder_OS.spec
```
where `OS` corresponds to a supported operating system.

The folder in the subdirectory `dist/` can be copied 
to other computers (maybe not even having Pylon 5 
or Python 3.6 installed) and contains a portable version
of this application.
