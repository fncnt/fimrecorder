# FIMRecorder

**THIS IS A PROTOTYPE! It does what it should. However, The code is far from pretty and I learned a lot while writing it.**

This program is
a simple recording application for FIM related
measurements. 
Currently, only Basler USB3 vision cameras recording in `Mono8` format are supported and only the model `acA1920-40um` has been tested.


## Documentation

You can find more detailed information in [`doc/fimdox.md`](https://github.com/fncnt/fimrecorder/blob/master/doc/fimdoc.md).

To create a `.pdf` file, simply run:
```
pandoc fimdoc.md -t latex -o fimdoc.pdf --number-sections --toc
```

## Usage
There are two different options to use this application.
Both of them require nearly the same setup:

### Prerequisites

At first, install [`python`](https://www.python.org/)

Install the following packages using `pip`:
- `pypylon`
- `PyQT5`
- `opencv-python`
- `vispy`

You may need to install `pypylon` [manually](https://github.com/basler/pypylon/blob/master/README.md#binary-installation) if you're using `python` versions above `3.6`.

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
