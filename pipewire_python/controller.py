"""
PIPEWIRE's Python controller (wrapper)

In the next pages you'll see documentation of each Python component
`controller.py`.
"""

# import warnings

# Loading constants Constants.py
from pipewire_python._constants import (
    MESSAGES_ERROR,
    RECOMMENDED_FORMATS,
    RECOMMENDED_RATES,
)

# Loading internal functions
from pipewire_python._utils import (
    _drop_keys_with_none_values,
    _execute_shell_command,
    _filter_by_type,
    _generate_command_by_dict,
    _generate_dict_interfaces,
    _generate_dict_list_targets,
    _get_dict_from_stdout,
)

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


class Controller:
    """
    Class that controls pipewire command line interface
    with shell commands, handling outputs, loading default
    configs and more.
    """

    _pipewire_cli = {  # Help
        "--help": "--help",  # -h
        "--version": "--version",
        "--remote": None,  # -r
    }

    _pipewire_modes = {  # Modes
        "--playback": None,  # -p
        "--record": None,  # -r
        "--midi": None,  # -m
    }

    _pipewire_list_targets = {  # "--list-targets": None,
        "list_playback": None,
        "list_record": None,
    }

    _pipewire_configs = {  # Configs
        "--media-type": None,  # *default=Audio
        "--media-category": None,  # *default=Playback
        "--media-role": None,  # *default=Music
        "--target": None,  # *default=auto
        "--latency": None,  # *default=100ms (SOURCE FILE if not specified)
        "--rate": None,  # *default=48000
        "--channels": None,  # [1,2] *default=2
        "--channel-map": None,  # ["stereo", "surround-51", "FL,FR"...] *default="FL,FR"
        "--format": None,  # [u8|s8|s16|s32|f32|f64] *default=s16
        "--volume": None,  # [0.0,1.0] *default=1.000
        "--quality": None,  # -q # [0,15] *default=4
        "--verbose": None,  # -v
    }

    _kill_pipewire = {
        "all": ["kill", "$(pidof pw-cat)"],
        "playback": ["kill", "$(pidof pw-play)"],
        "record": ["kill", "$(pidof pw-record)"],
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
        dict_default_values = _get_dict_from_stdout(
            stdout=str(stdout.decode()), verbose=verbose
        )

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
        self.load_list_targets(mode="playback", verbose=verbose)
        self.load_list_targets(mode="record", verbose=verbose)

    def _help_cli(
        self,
        # Debug
        verbose: bool = True,
    ):
        """Get pipewire command line help"""

        mycommand = ["pipewire", self._pipewire_cli["--help"]]

        stdout, _ = _execute_shell_command(command=mycommand, verbose=verbose)  # stderr

        return stdout

    def get_version(
        self,
        # Debug
        verbose: bool = False,
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

        mycommand = ["pw-cli", "--version"]

        if verbose:
            print(f"[mycommand]{mycommand}")

        stdout, _ = _execute_shell_command(
            command=mycommand, timeout=-1, verbose=verbose
        )
        versions = stdout.decode().split("\n")[1:]

        self._pipewire_cli["--version"] = versions

        return versions

    def verbose(
        self,
        status: bool = True,
    ):
        """Get full log of pipewire stream status with the command `pw-cat`

        An example of pw-cli usage is the code below:

        ```bash
        #!/bin/bash
        # For example
        pw-cat --playback beers.wav --verbose
        ```

        that will generate an output like this:

        ```bash
        opened file "beers.wav" format 00010002 channels:2 rate:44100
        using default channel map: FL,FR
        rate=44100 channels=2 fmt=s16 samplesize=2 stride=4 latency=4410 (0.100s)
        connecting playback stream; target_id=4294967295
        stream state changed unconnected -> connecting
        stream param change: id=2
        stream properties:
            media.type = "Audio"
            ...
        now=0 rate=0/0 ticks=0 delay=0 queued=0
        remote 0 is named "pipewire-0"
        core done
        stream state changed connecting -> paused
        stream param change: id=2
        ...
        stream param change: id=15
        stream param change: id=15
        now=13465394419270 rate=1/48000 ticks=35840 delay=512 queued=0
        now=13466525228363 rate=1/48000 ticks=90112 delay=512 queued=0
        ...
        stream drained
        stream state changed streaming -> paused
        stream param change: id=4
        stream state changed paused -> unconnected
        stream param change: id=4
        ```
        """

        if status:
            self._pipewire_configs["--verbose"] = "    "
        else:
            pass

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
            raise ValueError(
                f"{MESSAGES_ERROR['ValueError']}[target='{target}'] EMPTY VALUE"
            )
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
            raise ValueError(
                f"{MESSAGES_ERROR['ValueError']}[latency='{latency}'] EMPTY VALUE"
            )
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
            raise ValueError(
                f"{MESSAGES_ERROR['ValueError']}[rate='{rate}'] EMPTY VALUE"
            )
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
            raise ValueError(
                f"{MESSAGES_ERROR['ValueError']}[channels='{channels}'] EMPTY VALUE"
            )
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
            raise ValueError(
                f"{MESSAGES_ERROR['ValueError']}[_format='{_format}'] EMPTY VALUE"
            )
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
            raise ValueError(
                f"{MESSAGES_ERROR['ValueError']}[volume='{volume}'] EMPTY VALUE"
            )
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
            raise ValueError(
                f"{MESSAGES_ERROR['ValueError']}[volume='{volume}'] EMPTY VALUE"
            )

        # 12 - verbose cli
        if verbose:  # True
            self._pipewire_configs["--verbose"] = "    "
        else:
            pass

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

        if mode == "playback":
            mycommand = ["pw-cat", "--playback", "--list-targets"]
            stdout, _ = _execute_shell_command(
                command=mycommand, timeout=-1, verbose=verbose
            )
            self._pipewire_list_targets["list_playback"] = _generate_dict_list_targets(
                longstring=stdout.decode(), verbose=verbose
            )
        elif mode == "record":
            mycommand = ["pw-cat", "--record", "--list-targets"]
            stdout, _ = _execute_shell_command(
                command=mycommand, timeout=-1, verbose=verbose
            )
            self._pipewire_list_targets["list_record"] = _generate_dict_list_targets(
                longstring=stdout.decode(), verbose=verbose
            )
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
        "list_playback": {
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

    def get_list_interfaces(
        self,
        filtered_by_type: str = True,
        type_interfaces: str = "Client",
        # Debug
        verbose: bool = False,
    ):
        """Returns a list of applications currently using pipewire on Client.
        An example of pw-cli usage is the code below:

        ```bash
        #!/bin/bash
        pw-cli ls Client
        ```
        Args:
            filtered_by_type : If False, returns all. If not, returns a fitered dict
            type_interfaces : Set type of Interface
            ["Client","Link","Node","Factory","Module","Metadata","Endpoint",
            "Session","Endpoint Stream","EndpointLink","Port"]

        Returns:
            - dict_interfaces_filtered: dictionary
            with list of interfaces matching conditions

        Examples:
        ```python
        >>> Controller().get_list_interfaces()

        ```
        """
        mycommand = ["pw-cli", "info", "all"]

        # if verbose:
        #     print(f"[mycommand]{mycommand}")

        stdout, _ = _execute_shell_command(
            command=mycommand, timeout=-1, verbose=verbose
        )
        dict_interfaces = _generate_dict_interfaces(
            longstring=stdout.decode(), verbose=verbose
        )

        if filtered_by_type:
            dict_interfaces_filtered = _filter_by_type(
                dict_interfaces=dict_interfaces, type_interfaces=type_interfaces
            )
        else:
            dict_interfaces_filtered = dict_interfaces

        return dict_interfaces_filtered

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
        # warnings.warn("The name of the function may change on future releases", DeprecationWarning)

        mycommand = [
            "pw-cat",
            "--playback",
            audio_filename,
        ] + _generate_command_by_dict(mydict=self._pipewire_configs, verbose=verbose)

        if verbose:
            print(f"[mycommand]{mycommand}")

        stdout, stderr = _execute_shell_command(
            command=mycommand, timeout=-1, verbose=verbose
        )
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
        # warnings.warn("The name of the function may change on future releases", DeprecationWarning)

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
        """Function to stop process running under pipewire executed by
        python controller and with default process name of `pw-cat`, `pw-play` or `pw-record`.

        Args:
            mode (`str`) : string to kill process under `pw-cat`, `pw-play` or `pw-record`.

        Returns:
            - stdoutdict (`dict`) : a dictionary with keys of `mode`.

        Example with pipewire:
            pw-cat process
        """

        mycommand = self._kill_pipewire[mode]

        if verbose:
            print(f"[mycommands]{mycommand}")

        stdout, _ = _execute_shell_command(command=mycommand, verbose=verbose)

        return {mode: stdout}
