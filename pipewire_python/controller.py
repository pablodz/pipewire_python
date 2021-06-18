import asyncio
import json
import subprocess
import warnings

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

KEY_TO_REPLACE = "COMMAND_HERE"
PIPEWIRE_API_COMMANDS = {"play_default": ["pw-cat -p", "COMMAND_HERE"],
                         "record_default": ["pw-cat -r", "COMMAND_HERE"],
                         #  "play_default": ["pw-play", "COMMAND_HERE"],
                         #  "record_default": ["pw-record", "COMMAND_HERE"],
                         #  "cat": "pw-cat",  # Not implemented yet
                         "mon": "pw-mon",  # Not implemented yet
                         "dot": "pw-dot",  # Not implemented yet
                         "top": "pw-top",  # Not implemented yet
                         "dump": "pw-dump"  # Not implemented yet
                         }

MESSAGES_ERROR = {"NotImplementedError": "This function is not yet implemented",
                  "": ""}


class Player():

    commands_json = None

    def __init__(self):

        self.commands_json = PIPEWIRE_API_COMMANDS

    def play_wav_file(self,
                      # Test
                      audio_path: str,
                      # Debug
                      verbose: bool = False
                      ):
        """
        Execute pipewire command to play a WAV file

        Args:
            - audio_path (str): path of the file to be played.
            Example: 'audios/my_audio.wav'
        Return:
            - shell_result (str): shell response to the command
        """
        warnings.warn('The name of the function may change on future releases', DeprecationWarning)

        command = self.commands_json["play_default"]
        if verbose:
            print(command)
        # Replace COMMAND_HERE to fill the command
        command_structure = self._replace_key_by_command(key=KEY_TO_REPLACE,
                                                         command=command,
                                                         replace_value=audio_path)
        if verbose:
            print(command_structure)
        shell_subprocess = subprocess.Popen(command_structure,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT
                                            )
        stdout, stderr = shell_subprocess.communicate()
        self._print_std(stdout, stderr, verbose=verbose)
        return stdout, stderr

    async def play_wav_file_async(self,
                                  # Test
                                  audio_path: str,
                                  # Debug
                                  verbose: bool = False
                                  ):
        """
        [ASYNC] Execute pipewire command to play a WAV file

        Args:
            - audio_path (str): path of the file to be played.
            Example: 'audios/my_audio.wav'
        Return:
            - shell_result (str): shell response to the command
        """
        warnings.warn('The name of the function may change on future releases', DeprecationWarning)

        command = self.commands_json["play_default"]
        if verbose:
            print(command)
        # Replace COMMAND_HERE to fill the command
        command_structure = self._replace_key_by_command(key=KEY_TO_REPLACE,
                                                         command=command,
                                                         replace_value=audio_path)
        if verbose:
            print(command_structure)
        command_structure_joined = ' '.join(command_structure)
        if verbose:
            print(command_structure_joined)
            _ = await asyncio.gather(self._run_shell_async('ls -l',
                                                           verbose=verbose))
        # PIPEWIRE Returns None when play command is used
        _ = await asyncio.gather(self._run_shell_async(command_structure_joined,
                                                       verbose=verbose))

        return True

    def record_wav_file(self,
                        # Test
                        audio_path: str,
                        use_max_time: bool = True,
                        seconds_to_record: int = 5,
                        # Debug
                        verbose: bool = False
                        ):
        """
        Execute pipewire command to record a WAV file.
        By default one second with all pipewire default
        devices and properties selected.

        Args:
            - audio_path (str): path of the file to be played.
            Example: 'audios/my_audio.wav'
        Return:
            - shell_result (str): shell response to the command
        """
        warnings.warn('The name of the function may change on future releases', DeprecationWarning)

        command = self.commands_json["record_default"]
        # Replace COMMAND_HERE to fill the command
        command_structure = self._replace_key_by_command(key=KEY_TO_REPLACE,
                                                         command=command,
                                                         replace_value=audio_path)
        shell_subprocess = subprocess.Popen(command_structure,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT
                                            )
        try:
            stdout, stderr = shell_subprocess.communicate(timeout=seconds_to_record)
        except subprocess.TimeoutExpired as e:  # When script finish in time
            shell_subprocess.kill()
            stdout, stderr = shell_subprocess.communicate()

        self._print_std(stdout, stderr, verbose=verbose)
        return stdout, stderr

    async def record_wav_file_async(self,
                                    # Test
                                    audio_path: str,
                                    use_max_time: bool = True,
                                    seconds_to_record: int = 5,
                                    # Debug
                                    verbose: bool = False
                                    ):
        """
        [ASYNC] Execute pipewire command to record a WAV file.
        By default one second with all pipewire default
        devices and properties selected.

        Args:
            - audio_path (str): path of the file to be played.
            Example: 'audios/my_audio.wav'
        Return:
            - shell_result (str): shell response to the command
        """
        raise NotImplementedError('This function is not yet implemmented.')
        warnings.warn('The name of the function may change on future releases', DeprecationWarning)

        command = self.commands_json["record_default"]
        # Replace COMMAND_HERE to fill the command
        command_structure = self._replace_key_by_command(key=KEY_TO_REPLACE,
                                                         command=command,
                                                         replace_value=audio_path)

        if verbose:
            print(command_structure)
        command_structure_joined = ' '.join(command_structure)
        if verbose:
            print(command_structure_joined)
            _ = await asyncio.gather(self._run_shell_async('ls -l',
                                                           verbose=verbose))
        # PIPEWIRE Returns None when play command is used
        _ = await asyncio.gather(self._run_shell_async(command_structure_joined,
                                                       verbose=verbose))

        return True

    async def _run_shell_async(self,
                               # Test
                               cmd: list,
                               # Debug
                               verbose: bool = False
                               ):
        """
        [ASYNC] Function that execute shell commands in asyncio way

        Args:
            - cmd (str): command line to execute. Example: 'ls -l'
        Return:
            - shell_result (str): shell response to the command
        """
        proc = await asyncio.create_subprocess_shell(cmd,
                                                     stdout=asyncio.subprocess.PIPE,
                                                     stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        print(f'[{cmd!r} exited with {proc.returncode}]')
        self._print_std(stdout, stderr, verbose=verbose)

        return stdout, stderr

    async def _run_shell_async_timeout(self,
                                       timeout: int = 5,
                                       ):
        raise NotImplementedError('This function is not yet implemmented.')

        try:
            await asyncio.wait_for(print('Here the func'), timeout=timeout)
        except asyncio.TimeoutError:
            p.kill()
            await p.communicate()

    def _print_std(self,
                   # Debug
                   stdout: str,
                   stderr: str,
                   verbose: bool = False):

        if (stdout != None and verbose == True):
            print(f'[_print_std][stdout][type={type(stdout)}]\n{stdout.decode()}')
        if (stderr != None and verbose == True):
            print(f'[_print_std][stderr][type={type(stderr)}]\n{stderr.decode()}')

    def _replace_key_by_command(self,
                                # Test
                                key: str = KEY_TO_REPLACE,
                                command: str = '',
                                replace_value: str = '',
                                # Debug
                                verbose: bool = False):
        result = [item.replace(key, replace_value) for item in command]
        print(f'[KEY /COMMAND /REPLACE_VALUE] -> RESULT IS [{result}]')
        return result


class Controller():

    configs = {
        # Help
        "--help": None,  # -h
        "--version": None,
        "--verbose": None,  # -v
        # Configs
        "--remote": None,  # -r
        "--media-type": None,  # *default=Audio
        "--media-category": None,  # *default=Playback
        "--media-role": None,  # *default=Music
        "--target": None,  # *default=auto
        # [100ns,100us, 100ms,100s] *default=100ms (SOURCE FILE if not specified)
        "--latency": None,
        "--list-targets": None,
        # https://github.com/audiojs/sample-rate
        # [8000,11025,16000,22050,44100,48000,88200,96000,176400,192000,352800,384000] *default=48000
        "--rate": None,
        "--channels": None,  # [1,2] *default=2
        "--channel-map": None,  # ["stereo", "surround-51", "FL,FR"...] *default=unknown
        "--format": None,  # [u8|s8|s16|s32|f32|f64] *default=s16
        "--volume": None,  # [0.0,1.0] *default=1.0
        "--quality": None,  # -q # [0,15] *default=4
        # Modes
        "--playback": None,  # -p
        "--record": None,  # -r
        "--midi": None,  # -m
    }

    def __init__(self):
        """
        Constructor that get default parameters of pipewire command line
        interface and assign to variables to use in python controller
        """
        # super().__init__()
        # LOAD ALL DEFAULT PARAMETERS
        pass

    def _help(self):
        """
        Get pipewire command line help
        """

        raise NotImplementedError(MESSAGES_ERROR['NotImplementedError'])

    def version(self):
        """
        Get version of pipewire installed on OS.
        """

        raise NotImplementedError(MESSAGES_ERROR['NotImplementedError'])

    def verbose(self):

        raise NotImplementedError(MESSAGES_ERROR['NotImplementedError'])

    def set_config(self,
                   # configs
                   remote,
                   media_type,
                   media_category,
                   media_role,
                   target,
                   latency,
                   rate,
                   channels,
                   channel_map,
                   format,
                   volume,
                   quality,
                   ):
        """
        Set configuration to playback or record with pw-cat command.
        """

        raise NotImplementedError(MESSAGES_ERROR['NotImplementedError'])

    def list_targets(self,
                     mode,  # playback or record
                     ):
        """
        Returns a list of targets to playback or record. Then you can use
        the output to select a device to playback or record.
        """

        raise NotImplementedError(MESSAGES_ERROR['NotImplementedError'])

    def clear_devices(self,
                      mode: str = 'all', # ['all','playback','record']
                      # Debug
                      verbose: bool = False,
                      ):
        """
        Function to stop process running under pipewire.
        Example: pw-cat process
        """

        raise NotImplementedError(MESSAGES_ERROR['NotImplementedError'])

    def _execute_shell_command(self,
                               command: str,
                               timeout: int = -1,  # *default= no limit
                               # Debug
                               verbose: bool = False,
                               ):
        """
        Execute command on terminal via subprocess

        Args:
            - command (str): command line to execute. Example: 'ls -l'
            - timeout (int): (seconds) time to end the terminal process
            # Debug
            - verbose (bool): print variables for debug purposes
        Return:
            - stdout (str): terminal response to the command
            - stderr (str): terminal response to the command
        """
        # Create subprocess
        terminal_subprocess = subprocess.Popen(command,  # Example ['ls ','l']
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.STDOUT
                                               )
        # Execute command depending or not in timeout
        try:
            if timeout == -1:
                stdout, stderr = terminal_subprocess.communicate()
            else:
                stdout, stderr = terminal_subprocess.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:  # When script finish in time
            terminal_subprocess.kill()
            stdout, stderr = terminal_subprocess.communicate()

        # Print terminal output
        self._print_std(stdout,
                        stderr,
                        verbose=verbose)

        # Return terminal output
        return stdout, stderr

    async def _execute_shell_command_async(self,
                                           command: list,
                                           timeout:int=-1,
                                           # Debug
                                           verbose: bool = False
                                           ):
        """
        [ASYNC] Function that execute terminal commands in asyncio way

        Args:
            - command (str): command line to execute. Example: 'ls -l'
        Return:
            - stdout (str): terminal response to the command
            - stderr (str): terminal response to the command
        """
        if timeout==-1:
            # No timeout
            terminal_process_async = await asyncio.create_subprocess_shell(command,
                                                                        stdout=asyncio.subprocess.PIPE,
                                                                        stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await terminal_process_async.communicate()
            print(f'[_execute_shell_command_async]\
                    [{command!r} exited with\
                    {terminal_process_async.returncode}]')
            self._print_std(stdout,
                            stderr,
                            verbose=verbose)

            return stdout, stderr

    def _print_std(self,
                   # Debug
                   stdout: str,
                   stderr: str,
                   verbose: bool = False):
        """
        Print terminal output if are different to None and verbose activated
        """

        if (stdout != None and verbose == True):
            print(f'[_print_std][stdout][type={type(stdout)}]\n{stdout.decode()}')
        if (stderr != None and verbose == True):
            print(f'[_print_std][stderr][type={type(stderr)}]\n{stderr.decode()}')
