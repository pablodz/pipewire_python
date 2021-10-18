# ROADMAP

Things expected to implement:

Controller:
- [ ] Async and multiprocess support.
- [ ] Chunked data processing.
- [ ] Real time processing.
- [ ] Real time convert from wav to other encodings formats.
- [ ] Multiple players independently


Pipewire's API implementation:

- [x] Play `pw-play`
- [x] Record `pw-record`
- [ ] Cat `pw-cat`
- [ ] JACK-servers `pw-jack`
- [ ] pipewire command line.
- [ ] control over multiple pipewire cat running.
- [ ] `pw-mon` dumps and monitors the state of the PipeWire daemon
- [ ] `pw-dot` can dump a graph of the pipeline, check out the help for how to do this.
- [ ] `pw-top` monitors the real-time status of the graph. This is handy to find out what clients are running and how much DSP resources they use.
- [ ] `pw-dump` dumps the state of the PipeWire daemon in JSON format. This can be used to find out the properties and parameters of the objects in the PipeWire daemon.
- [x] `pw-cli ls Device` to list devices
- [ ] `pw-metadata` get metadata
- [ ] `pw-cli cn adapter factory.name=audiotestsrc media.class="Audio/Source" object.linger=1 node.name=my-null-source node.description="My null source"` Null sources can be created with the native API
- [ ] `pw-cli cn adapter factory.name=audiotestsrc media.class="Stream/Output/Audio" object.linger=1 node.name=my-sine-stream node.description="My sine stream" node.autoconnect=1` You can create a sine stream
- [ ] `pw-cli cn adapter factory.name=audiotestsrc media.class="Audio/Source" object.linger=1 node.name=my-sine-source node.description="My sine source"` Or a sine source
- [ ] `pw-cli s <card-id> Profile '{ index: <profile-index>, save: true }'` # set new default
- [ ] `pw-cli e <card-id> Profile` You can query the current profile with
- [x] `pw-cli ls Node`
- [ ] `pw-metadata 0 default.configured.audio.sink '{ "name": "<sink-name>" }'` You can change the configured defaults with

External aps

- [x] Easyeffects 

## Availability

- [X] PYPI package releases
- [X] CI/CD implementation


Graphic User Intefrace:
- [ ] GUI similar to `pavucontrol`, maybe `pwcontrol`.


> All APIS [here](https://docs.pipewire.org/page_api.html)

> More info [here](https://gitlab.freedesktop.org/pipewire/pipewire/-/tree/master)
