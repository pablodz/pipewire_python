"""
## Description

[PIPEWIRE](https://pipewire.org/) provides a low-latency, graph based processing engine
on top of audio and video devices that can be used to
support the use cases currently handled by both pulseaudio
and JACK. PipeWire was designed with a powerful security model
that makes interacting with audio and video devices from 
containerized applications easy, with supporting Flatpak
applications being the primary goal. Alongside Wayland and
Flatpak we expect PipeWire to provide a core building block 
for the future of Linux application development.

[pipewire_python](https://pypi.org/project/pipewire_python/) 
controlls `pipewire` via terminal, creating shell commands and executing them as required.

🎹 There are two ways to manage the python package:

1. NO_ASYNC: this way works as expected with delay time between 
`pipewire_python` and the rest of your code.

2. ASYNC: [⚠️Not yet implemented] this way works delegating the task to record or to play
a song file in background. Works with threads.

3. MULTIPROCESS: [⚠️Not yet implemented] Works with processes.


📄 More information about `pipewire` and it's API's:

- 🎵 Asyncio https://docs.python.org/3/library/asyncio-subprocess.html
- 🎵 Pipewire APIs https://www.linuxfromscratch.org/blfs/view/cvs/multimedia/pipewire.html
- 🎵 APIs example https://fedoraproject.org/wiki/QA:Testcase_PipeWire_PipeWire_CLI

Developed with ❤️ by Pablo Diaz & Anna Absi 


##  Install via
```bash

pip3 install pipewire_python # or pip
```

## Tutorial


```python
from pipewire_python.controller import Controller

# PLAYBACK: normal way
audio_controller = Controller()
audio_controller.set_config(rate=384000,
                            channels=2,
                            _format='f64',
                            volume=0.98,
                            quality=4,
                            # Debug
                            verbose=True)
audio_controller.playback(audio_filename='docs/beers.wav')

# RECORD: normal way
audio_controller = Controller(verbose=True)
audio_controller.record(audio_filename='docs/5sec_record.wav',
                        timeout_seconds=5,
                        # Debug
                        verbose=True)

```
"""

__version__ = "0.0.96"

import sys

if sys.platform == "linux":
    # from pipewire_python.controller import *
    pass
else:
    raise NotImplementedError("By now, Pipewire only runs on linux.")
