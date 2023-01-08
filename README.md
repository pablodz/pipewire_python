# PIPEWIRE's Python controller (wrapper)

[![PyPI Version][pypi-image]][pypi-url]
[![Build Status][build-image]][build-url]
[![publish_docs](https://github.com/pablodz/pipewire_python/actions/workflows/publish_docs.yml/badge.svg)](https://github.com/pablodz/pipewire_python/actions/workflows/publish_docs.yml)
[![publish_pypi](https://github.com/pablodz/pipewire_python/actions/workflows/publish_pypi.yml/badge.svg)](https://github.com/pablodz/pipewire_python/actions/workflows/publish_pypi.yml)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/pipewire_python.svg)][pypiversions-url]
[![codecov](https://codecov.io/gh/pablodz/pipewire_python/branch/main/graph/badge.svg?token=VN6O9QK3ZH)](https://codecov.io/gh/pablodz/pipewire_python)
[![Maintainability](https://api.codeclimate.com/v1/badges/fe82f8353628a4214abd/maintainability)](https://codeclimate.com/github/pablodz/pipewire_python/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/fe82f8353628a4214abd/test_coverage)](https://codeclimate.com/github/pablodz/pipewire_python/test_coverage)
[![Downloads](https://pepy.tech/badge/pipewire-python)](https://pepy.tech/project/pipewire-python)

JOIN OUR TELEGRAM SUPPORT:

[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/pipewire_python)

- **ONLY AUDIO BY NOW [PR & FR WELCOME]** 
- **STREAMING NOT SUPPORTED BY NOW**

<hr>

Python controller, player and recorder via pipewire's commands.

- [Pipewire](https://gitlab.freedesktop.org/pipewire/pipewire) is a project that aims to greatly improve handling of audio and video under Linux. (Better than pulseaudio or jack)

## Requirements

1. A Pipewire version installed (clean or via Pulseaudio) is needed, to check if you have pipewire installed and running, run this command, if the output is different, you'll need to [install pipewire](./docs/INSTALL_PIPEWIRE.md):

    1. Pipewire versions supported: 0.3.30, 0.3.32+

```bash
pw-cli info 0
```

```bash
# Example output
    id: 0
    permissions: rwxm
    type: PipeWire:Interface:Core/3
    cookie: 134115873
    user-name: "user"
    host-name: "user"
    version: "0.3.30" # Possibly more actual than this version
    name: "pipewire-0"
...
```

> To uninstall pipewire [click here](./docs/UNINSTALL_PIPEWIRE.md).

2.  Python 3.7+
3.  Ubuntu 20.04+

## Install & Tutorial

### Install

```bash
pip3 install pipewire_python # or pip
```

### Tutorial

#### PLAY AND RECORD

```python
from pipewire_python.controller import Controller

# [PLAYBACK]: normal way
audio_controller = Controller()
audio_controller.set_config(rate=384000,
                            channels=2,
                            _format='f64',
                            volume=0.98,
                            quality=4)
audio_controller.playback(audio_filename='docs/beers.wav')

# [RECORD]: normal way
audio_controller = Controller()
audio_controller.record(audio_filename='docs/5sec_record.wav',
                        timeout_seconds=5)
```
#### GET INTERFACES

```python
from pipewire_python.controller import Controller

audio_controller = Controller()
# Return all Client Interfaces on Pipewire
audio_controller.get_list_interfaces(
    type_interfaces="Client",
    filtered_by_type=True,
)
# Return all interfaces
audio_controller.get_list_interfaces(
    filtered_by_type=False,
)
```

#### LINK PORTS
### Linking Ports

```python
from pipewire_python import link

inputs = link.list_inputs()
outputs = link.list_outputs()

# Connect the last output to the last input -- during testing it was found that
# Midi channel is normally listed first, so this avoids that.
source = outputs[-1]
sink = inputs[-1]
source.connect(sink)

# Fun Fact! You can connect/disconnect in either order!
sink.disconnect(source) # Tada!

# Default Input/Output links will be made with left-left and right-right
# connections; in other words, a straight stereo connection.
# It's possible to manually cross the lines, however!
source.right.connect(sink.left)
source.left.connect(sink.right)
```


## Documentation

You can check the automatic build documentation [HERE](https://pablodz.github.io/pipewire_python/html/)

## Roadmap

Future implementations, next steps, API implementation and Control over Pipewire directly from python in the [ROADMAP](docs/ROADMAP.md).

## Contributions

PR, FR, and issues are welcome. Changes with PR in `dev` branch please due documentation runs after each commit in `main` branch. Check more [here](docs/NEW_RELEASE.md)

## License

[LICENSE](./LICENSE)

<!-- Badges -->

[pypi-image]: https://img.shields.io/pypi/v/pipewire_python
[pypi-url]: https://pypi.org/project/pipewire_python/
[build-image]: https://github.com/pablodz/pipewire_python/actions/workflows/build.yml/badge.svg
[build-url]: https://github.com/pablodz/pipewire_python/actions/workflows/build.yml
[coverage-image]: https://codecov.io/gh/pablodz/pipewire_python/branch/main/graph/badge.svg
[coverage-url]: https://codecov.io/gh/pablodz/pipewire_python
[quality-image]: https://api.codeclimate.com/v1/badges/3130fa0ba3b7993fbf0a/maintainability
[quality-url]: https://codeclimate.com/github/pablodz/pipewire_python
[pypiversions-url]: https://pypi.python.org/pypi/pipewire_python/
