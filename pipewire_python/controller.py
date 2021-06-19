"""
[DOCS]:
- Asyncio https://docs.python.org/3/library/asyncio-subprocess.html
- Pipewire APIs https://www.linuxfromscratch.org/blfs/view/cvs/multimedia/pipewire.html
- APIs example https://fedoraproject.org/wiki/QA:Testcase_PipeWire_PipeWire_CLI

[NO ASYNC]:
    subprocess

[ASYNC]:
    asyncio
"""

import asyncio
import warnings
from .utils import (
    _print_std,
    _get_dict_from_stdout,
    _update_dict_by_dict,
    _drop_keys_with_none_values,
    _generate_command_by_dict,
    _execute_shell_command,
)

# [FLAKE8] TO_AVOID_F401 PEP8
# https://stackoverflow.com/a/31079085/10491422
__all__ = [
    "_print_std",
    "_get_dict_from_stdout",
    "_update_dict_by_dict",
    "_drop_keys_with_none_values",
    "_generate_command_by_dict",
    "_execute_shell_command",
]

MESSAGES_ERROR = {
    "NotImplementedError": "This function is not yet implemented",
    "ValueError": "The value entered is wrong",
}

RECOMMENDED_RATES = [
    8000,
    11025,
    16000,
    22050,
    44100,
    48000,
    88200,
    96000,
    176400,
    192000,
    352800,
    384000,
]
RECOMMENDED_FORMATS = ["u8", "s8", "s16", "s32", "f32", "f64"]


class Controller:
    """
    Class that controlls pipewire command line interface with shell commands
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

    _pipewire_targets = {
        "--list-targets": None,
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
        """
        Constructor that get default parameters of pipewire command line
        interface and assign to variables to use in python controller
        """
        # super().__init__()
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

    def _help(self):
        """
        Get pipewire command line help
        """

        raise NotImplementedError(MESSAGES_ERROR["NotImplementedError"])

    def version(self):
        """
        Get version of pipewire installed on OS.
        """

        raise NotImplementedError(MESSAGES_ERROR["NotImplementedError"])

    def verbose(self):
        """
        Not implemented yet
        """

        raise NotImplementedError(MESSAGES_ERROR["NotImplementedError"])

    def get_config(self):
        """
        Return config dictionary with default or setup variables, remember that
        this object changes only on python-side. Is not updated on real time,
        For real-time, please create and destroy the class.
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
        """
        Set configuration to playback or record with pw-cat command.
        """
        # 1 - media_type
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

    def list_targets(
        self,
        mode,  # playback or record
    ):
        """
        Returns a list of targets to playback or record. Then you can use
        the output to select a device to playback or record.
        """

        raise NotImplementedError(MESSAGES_ERROR["NotImplementedError"])

    def playback(
        self,
        audio_filename: str = "myplayback.wav",
        # Debug
        verbose: bool = False,
    ):
        """
        Execute pipewire command to play an audio file

        Args:
            - audio_filename (str): path of the file to be played. *default='myplayback.wav'
        Return:
            - stdout (str): shell response to the command
            - stderr (str): shell response to the command
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
        """
        Execute pipewire command to record an audio file

        Args:
            - audio_filename (str): path of the file to be played. *default='myplayback.wav'
        Return:
            - stdout (str): shell response to the command
            - stderr (str): shell response to the command
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
        """
        Function to stop process running under pipewire.
        Example: pw-cat process
        """

        raise NotImplementedError(MESSAGES_ERROR["NotImplementedError"])

    async def _execute_shell_command_async(
        self,
        command,
        timeout: int = -1,
        # Debug
        verbose: bool = False,
    ):
        """
        [ASYNC] Function that execute terminal commands in asyncio way

        Args:
            - command (str): command line to execute. Example: 'ls -l'
        Return:
            - stdout (str): terminal response to the command
            - stderr (str): terminal response to the command
        """
        if timeout == -1:
            # No timeout
            terminal_process_async = await asyncio.create_subprocess_shell(
                command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await terminal_process_async.communicate()
            print(
                f"[_execute_shell_command_async]\
                    [{command!r} exited with\
                    {terminal_process_async.returncode}]"
            )
            _print_std(stdout, stderr, verbose=verbose)

        else:
            raise NotImplementedError(MESSAGES_ERROR["NotImplementedError"])

        return stdout, stderr
