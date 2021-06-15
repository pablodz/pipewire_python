# Python controller with pipewire

Python controller, player and recorder via pipewire's commands

- [Pipewire](https://gitlab.freedesktop.org/pipewire/pipewire) is a project that aims to greatly improve handling of audio and video under Linux. (Better than pulseaudio or jack)

## Requirements

1. A pipewire version installed (clean or via pulseaudio) is needed, to check if you have pipewire installed and running, run this command, if the output is different, you'll need to [install pipewire](./INSTALL_PIPEWIRE.md):
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
*	properties:
*		config.name = "pipewire.conf"
*		link.max-buffers = "16"
*		core.daemon = "true"
*		core.name = "pipewire-0"
*		cpu.max-align = "32"
*		clock.power-of-two-quantum = "true"
*		default.clock.rate = "48000"
*		default.clock.quantum = "1024"
*		default.clock.min-quantum = "32"
*		default.clock.max-quantum = "8192"
*		default.video.width = "640"
*		default.video.height = "480"
*		default.video.rate.num = "25"
*		default.video.rate.denom = "1"
*		mem.warn-mlock = "false"
*		mem.allow-mlock = "true"
*		object.id = "0"
```

## Tutorial

```python
from pipewire_python.pipewirecontroller import Player

player=Player()
player.play_WAV_File('docs/beers.wav')
```


## Pipewire's API implementation

- [X] Play `pw-play`
- [ ] Record `pw-record`
- [ ] Cat `pw-cat`
- [ ] JACK-servers `pw-jack`
- [ ] `pw-mon` dumps and monitors the state of the PipeWire daemon
- [ ] `pw-dot` can dump a graph of the pipeline, check out the help for
how to do this.
- [ ] `pw-top` monitors the real-time status of the graph. This is handy to
find out what clients are running and how much DSP resources they
use.
- [ ] `pw-dump` dumps the state of the PipeWire daemon in JSON format. This
can be used to find out the properties and parameters of the objects
in the PipeWire daemon.

## Availability

- [ ] Pypi package
- [ ] CI/CD implementation
- [ ] GUI controller



All APIS [here](https://docs.pipewire.org/page_api.html)

More info [here](https://gitlab.freedesktop.org/pipewire/pipewire/-/tree/master)

## Contributions

PR, FR and issues are welcome.

## License

[LICENSE](./LICENSE.md)