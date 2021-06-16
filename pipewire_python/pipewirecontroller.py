import asyncio
import json
import subprocess
import warnings

"""
Docs used:
- Asyncio https://docs.python.org/3/library/asyncio-subprocess.html
- Pipewire APIs https://www.linuxfromscratch.org/blfs/view/cvs/multimedia/pipewire.html

[NO ASYNC]:
    subprocess

[ASYNC]:
    asyncio
"""

KEY_TO_REPLACE = "COMMAND_HERE"
PIPEWIRE_API_COMMANDS = {"play_default": ["pw-play", "COMMAND_HERE"],
                         "record_default": ["pw-record", "COMMAND_HERE"],
                         "cat": "pw-cat",  # Not implemented yet
                         "mon": "pw-mon",  # Not implemented yet
                         "dot": "pw-dot",  # Not implemented yet
                         "top": "pw-top",  # Not implemented yet
                         "dump": "pw-dump"  # Not implemented yet
                         }


class Player:

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
