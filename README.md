# Python controller with pipewire

[![PyPI Version][pypi-image]][pypi-url]
[![Build Status][build-image]][build-url]
[![Publish Status][publish-image]][publish-url]
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/pipewire_python.svg)][pypiversions-url]
[![Code Coverage][coverage-image]][coverage-url]
[![Code Quality][quality-image]][quality-url]

Python controller, player and recorder via pipewire's commands

- [Pipewire](https://gitlab.freedesktop.org/pipewire/pipewire) is a project that aims to greatly improve handling of audio and video under Linux. (Better than pulseaudio or jack)

## Requirements

1. A pipewire version installed (clean or via pulseaudio) is needed, to check if you have pipewire installed and running, run this command, if the output is different, you'll need to [install pipewire](./docs/INSTALL_PIPEWIRE.md):

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

> To uninstall pipewire [clic here](./docs/UNINSTALL_PIPEWIRE.md).

2.  Python 3.7+
3.  Ubuntu 20.04+

## Install & Tutorial

### Install

```bash
pip3 install pipewire_python # or pip
```

### Tutorial

```python
from pipewire_python.pipewirecontroller import Player
import asyncio

# Download sample audio

#########################
# PLAYBACK              #
#########################
# normal way
player = Player()
player.play_wav_file('docs/beers.wav',
                     verbose=True)

# async way
player = Player()
asyncio.run(player.play_wav_file_async('docs/beers.wav',
                                       verbose=True))

#########################
# RECORD [default=5sec] #
#########################

# normal way
player = Player()
player.record_wav_file('docs/5sec_record.wav',
                       verbose=True)

# async way
player = Player()
asyncio.run(player.record_wav_file_async('docs/5sec_record.wav',
                                         verbose=True))

```


## ROADMAP

Future implementations, next steps, API implementation and Control over pipewire directly from python in the [ROADMAP](docs/ROADMAP.md).


## Contributions

PR, FR and issues are welcome.

## License

[LICENSE](./LICENSE)

<!-- Badges -->

[pypi-image]: https://img.shields.io/pypi/v/pipewire_python
[pypi-url]: https://pypi.org/project/pipewire_python/
[build-image]: https://github.com/pablodz/pipewire_python/actions/workflows/build.yml/badge.svg
[build-url]: https://github.com/pablodz/pipewire_python/actions/workflows/build.yml
[publish-image]: https://github.com/pablodz/pipewire_python/actions/workflows/publish.yml/badge.svg
[publish-url]: https://github.com/pablodz/pipewire_python/actions/workflows/publish.yml
[coverage-image]: https://codecov.io/gh/pablodz/pipewire_python/branch/main/graph/badge.svg
[coverage-url]: https://codecov.io/gh/pablodz/pipewire_python
[quality-image]: https://api.codeclimate.com/v1/badges/3130fa0ba3b7993fbf0a/maintainability
[quality-url]: https://codeclimate.com/github/pablodz/pipewire_python
[pypiversions-url]: https://pypi.python.org/pypi/pipewire_python/
