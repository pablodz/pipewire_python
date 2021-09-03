"""
Here we store internal functions, don't expect
to see something here in documentation html version.
"""
import subprocess
import asyncio
import re

# Loading constants Constants.py
from ._constants import MESSAGES_ERROR


def _print_std(
    stdout: bytes,
    stderr: bytes,
    # Debug
    verbose: bool = False,
):
    """
    Print terminal output if are different to None and verbose activated
    """

    if stdout is not None and verbose:
        print(f"[_print_std][stdout][type={type(stdout)}]\n{stdout.decode()}")
    if stderr is not None and verbose:
        print(f"[_print_std][stderr][type={type(stderr)}]\n{stderr.decode()}")


def _get_dict_from_stdout(
    stdout: str,
    # Debug
    verbose: bool = False,
):
    """
    Converts shell output (str) to dictionary looking for
    "default" and "--" values
    """

    rows = stdout.split("\n")
    config_dict = {}
    for row in rows:
        if "default" in row:
            key = "--" + row.split("--")[1].split(" ")[0]
            value = row.split("default ")[1].replace(")", "")
            config_dict[key] = value
    if verbose:
        print(config_dict)
    return config_dict


def _update_dict_by_dict(
    main_dict: dict,
    secondary_dict: dict,
):
    """
    Update values of one dictionary with values of another dictionary
    based on keys
    """
    return main_dict.update(([(key, secondary_dict[key]) for key in secondary_dict.keys()]))


def _drop_keys_with_none_values(main_dict: dict):
    """
    Drop keys with None values to parse safe dictionary config
    """
    return {k: v for k, v in main_dict.items() if v is not None}


def _generate_command_by_dict(
    mydict: dict,
    # Debug
    verbose: bool = False,
):
    """
    Generate an array based on dictionary with keys and values
    """
    array_command = []
    # append to a list
    for key, value in mydict.items():
        array_command.extend([key, value])
    if verbose:
        print(array_command)
    # return values
    return array_command


def _execute_shell_command(
    command: list[str],
    timeout: int = -1,  # *default= no limit
    # Debug
    verbose: bool = False,
):
    """
    Execute command on terminal via subprocess

    Args:
        - command (str): command line to execute. Example: 'ls -l'
        - timeout (int): (seconds) time to end the terminal process
        - verbose (bool): print variables for debug purposes
    Return:
        - stdout (str): terminal response to the command
        - stderr (str): terminal response to the command
    """
    # Create subprocess
    # NO-RESOURCE-ALLOCATING
    # terminal_subprocess = subprocess.Popen(
    #     command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT  # Example ['ls ','l']
    # )

    with subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT  # Example ['ls ','l']
    ) as terminal_subprocess:
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
        _print_std(stdout, stderr, verbose=verbose)

        # Return terminal output
        return stdout, stderr


async def _execute_shell_command_async(
    command,
    timeout: int = -1,
    # Debug
    verbose: bool = False,
):
    """[ASYNC] Function that execute terminal commands in asyncio way

    Args:
        - command (str): command line to execute. Example: 'ls -l'
    Return:
        - stdout (str): terminal response to the command.
        - stderr (str): terminal response to the command.
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


def _generate_dict_list_targets(
    longstring: str,  # string output of shell
    # Debug
    verbose: bool = False,
):
    """
    Function that transform long string of list targets
    to a `dict`
    """

    regex_id = r"(\d.*):"
    regex_desc = r'description="([^"]*)"'
    regex_prio = r"prio=(-?\d.*)"
    regex_default_node = r"[*]\t(\d\d)"
    regex_alsa_node = r"(alsa_[a-zA-Z].*)"

    results_regex_id = re.findall(regex_id, longstring)
    results_regex_desc = re.findall(regex_desc, longstring)
    results_regex_prio = re.findall(regex_prio, longstring)
    results_regex_default_node = re.findall(regex_default_node, longstring)
    results_regex_alsa_mode = re.findall(regex_alsa_node, longstring)

    mydict = {}
    for idx, _ in enumerate(results_regex_id):
        mydict[results_regex_id[idx]] = {
            "description": results_regex_desc[idx],
            "prior": results_regex_prio[idx],
        }
    mydict["_list_nodes"] = results_regex_id
    mydict["_node_default"] = results_regex_default_node
    mydict["_alsa_node"] = results_regex_alsa_mode

    if verbose:
        print(mydict)

    return mydict
