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

Tutorial [here](https://github.com/pablodz/pipewire_python/blob/main/README.py)

<hr>
## Documentation

In the next pages you'll see documentation of each python component.
"""

import warnings

# Loading internal functions
from ._utils import (_drop_keys_with_none_values,
                    _execute_shell_command,
                    _generate_command_by_dict,
                    _get_dict_from_stdout,
                    _print_std, _update_dict_by_dict,
                    _generate_dict_list_targets)

# Loading constants Constants.py
from ._constants import (MESSAGES_ERROR,
                        RECOMMENDED_FORMATS,
                        RECOMMENDED_RATES)

# [DEPRECATED] [FLAKE8] TO_AVOID_F401 PEP8
# [DEPRECATED] https://stackoverflow.com/a/31079085/10491422
# NOW USED IN DOCUMENTATION
# __all__ = [
#     # Classes and fucntions to doc
#     'Controller',
#     # [DEPRECATED] Unused files pylint
#     # "_print_std",
#     # "_get_dict_from_stdout",
#     # "_update_dict_by_dict",
#     # "_drop_keys_with_none_values",
#     # "_generate_command_by_dict",
#     # "_execute_shell_command",
# ]


class Controller():
    """
    Class that controls pipewire command line interface
    with shell commands, handling outputs, loading default
    configs and more.
    """

    _pipewire_cli = {  # Help
        "--help": None,  # -h
        "--version": None,
        "--verbose": None,  # -v
        "--remote": None,  # -r
    }

    _pipewire_modes = {  # Modes
        "--playback": None,  # -p
        "--record": None,  # -r
        "--midi": None,  # -m
    }

    _pipewire_list_targets = {  # "--list-targets": None,

    }

    _pipewire_configs = {  # Configs
        "--media-type": None,  # *default=Audio
        "--media-category": None,  # *default=Playback
        "--media-role": None,  # *default=Music
        "--target": None,  # *default=auto
        "--latency": None,  # *default=100ms (SOURCE FILE if not specified)
        "--rate": None,  # *default=48000
        "--channels": None,  # [1,2] *default=2
        "--channel-map": None,  # ["stereo", "surround-51", "FL,FR"...] *default=unknown
        "--format": None,  # [u8|s8|s16|s32|f32|f64] *default=s16
        "--volume": None,  # [0.0,1.0] *default=1.000
        "--quality": None,  # -q # [0,15] *default=4
    }

    def __init__(
        self,
        # Debug
        verbose: bool = False,
    ):
        """This constructor load default configs from OS executing
        the following pipewire command

        ```bash
        #!/bin/bash
        # Get defaults from output of:
        pw-cat -h
        ```
        """
        # LOAD ALL DEFAULT PARAMETERS

        mycommand = ["pw-cat", "-h"]

        # get default parameters with help
        stdout, _ = _execute_shell_command(command=mycommand, verbose=verbose)  # stderr
        # convert stdout to dictionary
        dict_default_values = _get_dict_from_stdout(stdout=str(stdout.decode()), verbose=verbose)

        if verbose:
            print(self._pipewire_configs)

        # Save default system configs to our json
        self._pipewire_configs.update(
            ([(key, dict_default_values[key]) for key in dict_default_values])
        )

        if verbose:
            print(self._pipewire_configs)

        # Delete keys with None values
        self._pipewire_configs = _drop_keys_with_none_values(self._pipewire_configs)

        if verbose:
            print(self._pipewire_configs)

        # Load values of list targets
        self.load_list_targets(mode='playback', verbose=verbose)
        self.load_list_targets(mode='record', verbose=verbose)

    def _help(self):
        """Get pipewire command line help
        """

        raise NotImplementedError(MESSAGES_ERROR["NotImplementedError"])

    def get_version(self,
                    verbose: bool = False
                    ):
        """Get version of pipewire installed on OS by executing the following
        code:

        ```bash
        #!/bin/bash
        pw-cli --version
        ```

        Args:
            verbose (bool) : True enable debug logs. *default=False

        Returns:
            - versions (list) : Versions of pipewire compiled
        """

        mycommand = ['pw-cli', '--version']

        if verbose:
            print(f"[mycommand]{mycommand}")

        stdout, _ = _execute_shell_command(command=mycommand, timeout=-1, verbose=verbose)
        versions = stdout.decode().split('\n')[1:]
        return versions

    def verbose(self):
        """[⚠️NOT IMPLEMENTED YET]

        Get full log of pipewire stream status with the following command

        ```bash
        #!/bin/bash
        # For example
        pw-cat --playback beers.wav --verbose
        ```

        will generate an output like this:

        ```bash
        opened file "beers.wav" format 00010002 channels:2 rate:44100
        using default channel map: FL,FR
        rate=44100 channels=2 fmt=s16 samplesize=2 stride=4 latency=4410 (0.100s)
        connecting playback stream; target_id=4294967295
        stream state changed unconnected -> connecting
        stream param change: id=2
        stream properties:
            media.type = "Audio"
            media.category = "Playback"
            media.role = "Music"
            application.name = "pw-cat"
            media.filename = "beers.wav"
            media.name = "beers.wav"
            node.name = "pw-cat"
            media.software = "Lavf58.33.100"
            media.format = "WAV (Microsoft)"
            node.latency = "4410/44100"
            stream.is-live = "true"
            node.autoconnect = "true"
            media.class = "Stream/Output/Audio"
        now=0 rate=0/0 ticks=0 delay=0 queued=0
        remote 0 is named "pipewire-0"
        core done
        stream state changed connecting -> paused
        stream param change: id=2
        stream param change: id=15
        stream param change: id=15
        stream param change: id=4
        stream state changed paused -> streaming
        stream param change: id=2
        set stream volume to 1.000 - success
        stream node 73
        stream param change: id=15
        stream param change: id=15
        now=13465394419270 rate=1/48000 ticks=35840 delay=512 queued=0
        now=13466525228363 rate=1/48000 ticks=90112 delay=512 queued=0
        now=13467250652784 rate=1/48000 ticks=124928 delay=512 queued=0
        now=13468381462104 rate=1/48000 ticks=179200 delay=512 queued=0
        now=13469490934155 rate=1/48000 ticks=232448 delay=512 queued=0
        now=13470600406171 rate=1/48000 ticks=285696 delay=512 queued=0
        now=13471347166416 rate=1/48000 ticks=321536 delay=512 queued=0
        stream drained
        stream state changed streaming -> paused
        stream param change: id=4
        stream state changed paused -> unconnected
        stream param change: id=4

        ```
        """

        raise NotImplementedError(MESSAGES_ERROR["NotImplementedError"])

    def get_config(self):
        """Return config dictionary with default or setup variables, remember that
        this object changes only on python-side. Is not updated on real time,
        For real-time, please create and destroy the class.

        Args:
            Nothing

        Returns:
            - _pipewire_configs (`dict`) : dictionary with config values

        """

        return self._pipewire_configs

    def set_config(
        self,
        # configs
        media_type=None,
        media_category=None,
        media_role=None,
        target=None,
        latency=None,
        rate=None,
        channels=None,
        channels_map=None,
        _format=None,
        volume=None,
        quality=None,
        # Debug
        verbose=False,
    ):
        """Method that get args as variables and set them
        to the `json` parameter of the class `_pipewire_configs`,
        then you can use in other method, such as `playback(...)` or 
        `record(...)`. This method verifies values to avoid wrong
        settings.

        Args:
            media_type : Set media type
            media_category : Set media category
            media_role : Set media role
            target : Set node target 
            latency : Set node latency *example=100ms
            rate : Set sample rate [8000,11025,16000,22050,44100,48000,88200,96000,176400,192000,352800,384000]
            channels : Numbers of channels [1,2]
            channels_map : ["stereo", "surround-51", "FL,FR", ...]
            _format : ["u8", "s8", "s16", "s32", "f32", "f64"] 
            volume : Stream volume [0.000, 1.000]
            quality : Resampler quality [0, 15]
            verbose (`bool`): True enable debug logs. *default=False

        Returns:
            - Nothing

        More:
            Check all links listed at the beginning of this page

        """  # 1 - media_type
        if media_type:
            self._pipewire_configs["--media-type"] = str(media_type)
        elif media_type is None:
            pass
        else:
            raise ValueError(
                f"{MESSAGES_ERROR['ValueError']}[media_type='{media_type}'] EMPTY VALUE"
            )
        # 2 - media_category
        if media_category:
            self._pipewire_configs["--media-category"] = str(media_category)
        elif media_category is None:
            pass
        else:
            raise ValueError(
                f"{MESSAGES_ERROR['ValueError']}[media_category='{media_category}'] EMPTY VALUE"
            )
        # 3 - media_role
        if media_role:
            self._pipewire_configs["--media-role"] = str(media_role)
        elif media_role is None:
            pass
        else:
            raise ValueError(
                f"{MESSAGES_ERROR['ValueError']}[media_role='{media_role}'] EMPTY VALUE"
            )
        # 4 - target
        if target:
            self._pipewire_configs["--target"] = str(target)
        elif target is None:
            pass
        else:
            raise ValueError(f"{MESSAGES_ERROR['ValueError']}[target='{target}'] EMPTY VALUE")
        # 5 - latency
        if latency:
            if any(chr.isdigit() for chr in latency):  # Contain numbers
                self._pipewire_configs["--latency"] = str(latency)
            else:
                raise ValueError(
                    f"{MESSAGES_ERROR['ValueError']}[latency='{latency}'] NO NUMBER IN VARIABLE"
                )
        elif latency is None:
            pass
        else:
            raise ValueError(f"{MESSAGES_ERROR['ValueError']}[latency='{latency}'] EMPTY VALUE")
        # 6 - rate
        if rate:
            if rate in RECOMMENDED_RATES:
                self._pipewire_configs["--rate"] = str(rate)
            else:
                raise ValueError(
                    f"{MESSAGES_ERROR['ValueError']}[rate='{rate}']\
                         VALUE NOT IN RECOMMENDED LIST \n{RECOMMENDED_RATES}"
                )
        elif rate is None:
            pass
        else:
            raise ValueError(f"{MESSAGES_ERROR['ValueError']}[rate='{rate}'] EMPTY VALUE")
        # 7 - channels
        if channels:
            if channels in [1, 2]:  # values
                self._pipewire_configs["--channels"] = str(channels)
            else:
                raise ValueError(
                    f"{MESSAGES_ERROR['ValueError']}[channels='{channels}']\
                         WRONG VALUE\n ONLY 1 or 2."
                )
        elif channels is None:
            pass
        else:
            raise ValueError(f"{MESSAGES_ERROR['ValueError']}[channels='{channels}'] EMPTY VALUE")
        # 8 - channels-map
        if channels_map:
            self._pipewire_configs["--channels-map"] = str(channels_map)
        elif channels_map is None:
            pass
        else:
            raise ValueError(
                f"{MESSAGES_ERROR['ValueError']}[channels_map='{channels_map}'] EMPTY VALUE"
            )
        # 9 - format
        if _format:
            if _format in RECOMMENDED_FORMATS:
                self._pipewire_configs["--format"] = str(_format)
            else:
                raise ValueError(
                    f"{MESSAGES_ERROR['ValueError']}[_format='{_format}']\
                         VALUE NOT IN RECOMMENDED LIST \n{RECOMMENDED_FORMATS}"
                )
        elif _format is None:
            pass
        else:
            raise ValueError(f"{MESSAGES_ERROR['ValueError']}[_format='{_format}'] EMPTY VALUE")
        # 10 - volume
        if volume:
            if 0.0 <= volume <= 1.0:
                self._pipewire_configs["--volume"] = str(volume)
            else:
                raise ValueError(
                    f"{MESSAGES_ERROR['ValueError']}[volume='{volume}']\
                         OUT OF RANGE \n [0.000, 1.000]"
                )
        elif volume is None:
            pass
        else:
            raise ValueError(f"{MESSAGES_ERROR['ValueError']}[volume='{volume}'] EMPTY VALUE")
        # 11 - quality
        if quality:
            if 0 <= quality <= 15:
                self._pipewire_configs["--quality"] = str(quality)
            else:
                raise ValueError(
                    f"{MESSAGES_ERROR['ValueError']}[quality='{quality}'] OUT OF RANGE \n [0, 15]"
                )
        elif quality is None:
            pass
        else:
            raise ValueError(f"{MESSAGES_ERROR['ValueError']}[volume='{volume}'] EMPTY VALUE")

        if verbose:
            print(self._pipewire_configs)

    def load_list_targets(
        self,
        mode,  # playback or record
        # Debug,
        verbose: bool = False,
    ):
        """Returns a list of targets to playback or record. Then you can use
        the output to select a device to playback or record.
        """

        if mode == 'playback':
            mycommand = ['pw-cat', '--playback', '--list-targets']
            stdout, _ = _execute_shell_command(command=mycommand, timeout=-1, verbose=verbose)
            self._pipewire_list_targets['list_playblack'] = _generate_dict_list_targets(longstring=stdout.decode(),
                                                                                        verbose=verbose)
        elif mode == 'record':
            mycommand = ['pw-cat', '--record', '--list-targets']
            stdout, _ = _execute_shell_command(command=mycommand, timeout=-1, verbose=verbose)
            self._pipewire_list_targets['list_record'] = _generate_dict_list_targets(longstring=stdout.decode(),
                                                                                     verbose=verbose)
        else:
            raise AttributeError(MESSAGES_ERROR["ValueError"])

        if verbose:
            print(f"[mycommand]{mycommand}")

    def get_list_targets(
        self,
        # Debug,
        verbose: bool = False,
    ):
        """Returns a list of targets to playback or record. Then you can use
        the output to select a device to playback or record.

        Returns:
            - `_pipewire_list_targets`

        Examples:
        ```python
        >>> Controller().get_list_targets()
        {
        "list_playblack": {
            "86": {
            "description": "Starship/Matisse HD Audio Controller Pro",
            "prior": "936"
            },
            "_list_nodes": [
            "86"
            ],
            "_node_default": [
            "86"
            ],
            "_alsa_node": [
            "alsa_output.pci-0000_0a_00.4.pro-output-0"
            ]
        },
        "list_record": {
            "86": {
            "description": "Starship/Matisse HD Audio Controller Pro",
            "prior": "936"
            },
            "_list_nodes": [
            "86"
            ],
            "_node_default": [
            "86"
            ],
            "_alsa_node": [
            "alsa_output.pci-0000_0a_00.4.pro-output-0"
            ]
        }
        }
        ```
        """

        if verbose:
            print(self._pipewire_list_targets)
        return self._pipewire_list_targets

    def playback(
        self,
        audio_filename: str = "myplayback.wav",
        # Debug
        verbose: bool = False,
    ):
        """Execute pipewire command to play an audio file with the following
        command:

        ```bash
        #!/bin/bash
        pw-cat --playback {audio_filename} + {configs}
        # configs are a concatenated params
        ```

        Args:
            audio_filename (`str`): Path of the file to be played. *default='myplayback.wav'
            verbose (`bool`): True enable debug logs. *default=False

        Returns:
            - stdout (`str`): Shell response to the command in stdout format
            - stderr (`str`): Shell response response to the command in stderr format
        """
        warnings.warn("The name of the function may change on future releases", DeprecationWarning)

        mycommand = ["pw-cat", "--playback", audio_filename] + _generate_command_by_dict(
            mydict=self._pipewire_configs, verbose=verbose
        )

        if verbose:
            print(f"[mycommand]{mycommand}")

        stdout, stderr = _execute_shell_command(command=mycommand, timeout=-1, verbose=verbose)
        return stdout, stderr

    def record(
        self,
        audio_filename: str = "myplayback.wav",
        timeout_seconds=5,
        # Debug
        verbose: bool = False,
    ):
        """Execute pipewire command to record an audio file, with a timeout of 5
        seconds with the following code and exiting the shell when tiomeout is over.

        ```bash
        #!/bin/bash
        pw-cat --record {audio_filename}
        # timeout is managed by python3 (when signal CTRL+C is sended)
        ```

        Args:
            audio_filename (`str`): Path of the file to be played. *default='myplayback.wav'
            verbose (`bool`): True enable debug logs. *default=False

        Returns:
            - stdout (`str`): Shell response to the command in stdout format
            - stderr (`str`): Shell response response to the command in stderr format
        """
        warnings.warn("The name of the function may change on future releases", DeprecationWarning)

        mycommand = ["pw-cat", "--record", audio_filename] + _generate_command_by_dict(
            mydict=self._pipewire_configs, verbose=verbose
        )

        if verbose:
            print(f"[mycommand]{mycommand}")

        stdout, stderr = _execute_shell_command(
            command=mycommand, timeout=timeout_seconds, verbose=verbose
        )
        return stdout, stderr

    def clear_devices(
        self,
        mode: str = "all",  # ['all','playback','record']
        # Debug
        verbose: bool = False,
    ):
        """[⚠️NOT IMPLEMENTED YET] 
        Function to stop process running under pipewire.
        Example: pw-cat process
        """

        raise NotImplementedError(MESSAGES_ERROR["NotImplementedError"])
