"""
PIPEWIRE's Python controller (wrapper)

In the next pages you'll see documentation of each Python component
`link.py`.
"""

from typing import List, Union
from dataclasses import dataclass
from enum import Enum

from ._utils import (
    _execute_shell_command,
)


PW_LINK_COMMAND = "pw-link"


class InvalidLink(ValueError):
    """Invalid link configuration."""

class ChannelType(Enum):
    """Pipewire Channel Type - Input or Output."""
    INPUT = 1
    OUTPUT = 2


@dataclass
class Channel:
    """
    Pipewire Link Channel Object.

    Connect or disconnect Pipewire links with unique individual channels.

    Attributes
    ----------
    id:             int
                    Pipewire channel identifier.
    device:         str
                    Pipewire device name.
    name:           str
                    Pipewire device channel name, (typically uses L or R).
    channel_type:   ChannelType
    """

    device: str
    name: str
    id: int
    channel_type: ChannelType

    def _join_arguments(self, other: "Channel", message: str) -> List[str]:
        """Generate a list of arguments to appropriately set output, then input
        for the connection/disconnection command."""
        args = [PW_LINK_COMMAND]
        if self.channel_type == ChannelType.INPUT:
            if other.channel_type == ChannelType.INPUT:
                raise InvalidLink(message.format("input"))
            # Valid -- Append the Output (other) First
            args.append(":".join((other.device, other.name)))
            args.append(":".join((self.device, self.name)))
        else:
            if other.channel_type == ChannelType.OUTPUT:
                raise InvalidLink(message.format("output"))
            # Valid -- Append the Output (self) First
            args.append(":".join((self.device, self.name)))
            args.append(":".join((other.device, other.name)))
        return args

    def connect(self, other: "Channel"):
        """Connect this channel to another channel."""
        args = self._join_arguments(
            other=other,
            message="Cannot connect an {} to another {}."
        )
        stdout, stderr = _execute_shell_command(args)
    
    def disconnect(self, other: "Channel"):
        """Disconnect this channel from another."""
        args = self._join_arguments(
            other=other,
            message="Cannot disconnect an {} from another {}."
        )
        args.append("--disconnect")
        stdout, stderr = _execute_shell_command(args)


@dataclass
class Input:
    """
    Pipewire Input Object.

    Grouping of left and right channels for a Pipewire link input.

    Attributes
    ----------
    left:   Channel
            Left (or mono) channel.
    right:  Channel
            Right channel.
    """

    left: Channel
    right: Channel

    def connect(self, output_device: "Output") -> Union["Link", None]:
        """Connect this input to an output."""
        connections = 0
        if self.left and output_device.left:
            self.left.connect(output_device.left)
            connections += 1
        if self.right and output_device.right:
            self.right.connect(output_device.right)
            connections += 1
        if connections > 0:
            return Link(input=self, output=output_device)
    
    def disconnect(self, output_device: Union["Output", "Link"]):
        """Disconnect this input from an output."""
        if self.left and output_device.left:
            self.left.disconnect(output_device.left)
        if self.right and output_device.right:
            self.right.disconnect(output_device.right)


@dataclass
class Output:
    """
    Pipewire Output Object.

    Grouping of left and right channels for a Pipewire link output.

    Attributes
    ----------
    left:   Channel
            Left (or mono) channel.
    right:  Channel
            Right channel.
    """

    left: Channel
    right: Channel

    def connect(self, input_device: "Input") -> Union["Link", None]:
        """Connect this input to an output."""
        connections = 0
        if self.left and input_device.left:
            self.left.connect(input_device.left)
            connections += 1
        if self.right and input_device.right:
            self.right.connect(input_device.right)
            connections += 1
        if connections > 0:
            return Link(input=self, output=input_device)
    
    def disconnect(self, input_device: Union["Input", "Link"]):
        """Disconnect this input from an output."""
        if self.left and input_device.left:
            self.left.disconnect(input_device.left)
        if self.right and input_device.right:
            self.right.disconnect(input_device.right)


@dataclass
class Link:
    """
    Pipewire Link Object.

    Configured Pipewire link between an input and output device.

    Attributes
    ----------
    input:  Input
            Pipewire input object connected with link.
    output: Output
            Pipewire output object connected with link.
    """

    input: Input
    output: Output

    def disconnect(self):
        """Disconnect the Link."""
        self.input.disconnect(self.output)


def _split_id_from_name(command) -> List[List[str]]:
    """Helper function to generate a list of channels"""
    stdout, _ = _execute_shell_command([PW_LINK_COMMAND, command, "--id"])
    data_sets = []
    for channel in stdout.decode('utf-8').split("\n"):
        channels = channel.lstrip().split(" ", maxsplit=1)
        if len(channels) == 2:
            data_sets.append(channels)
    return data_sets


def list_inputs() -> List[Input]:
    """List the Inputs."""
    channels = []
    for channel_id, channel_data in _split_id_from_name("--input"):
        device, name = channel_data.split(':', maxsplit=1)
        channels.append(
            Channel(
                id=channel_id,
                device=device,
                name=name,
                channel_type=ChannelType.INPUT
            )
        )
    i = 0
    num_channels = len(channels)
    inputs = []
    # Review the list of Channels to Pair Appropriate Channels into an Input
    while i < num_channels:
        i += 1
        if i+1 <= num_channels:
            # If this channel device is the same as the next channel's device
            if channels[i].device == channels[i-1].device:
                # Identify Left and Right Channels
                if "FL" in channels[i].name.upper():
                    inputs.append(Input(
                        left = channels[i],
                        right = channels[i-1]
                    ))
                    i += 1
                    continue
                elif "FR" in channels[i].name.upper():
                    inputs.append(Input(
                        right = channels[i],
                        left = channels[i-1]
                    ))
                    i += 1
                    continue
        # Use Left-Channel Only if there's no left/right
        inputs.append(Input(left=channels[i-1], right=None))
    return inputs


def list_outputs() -> List[Output]:
    """List the Outputs."""
    channels = []
    for channel_id, channel_data in _split_id_from_name("--output"):
        device, name = channel_data.split(':', maxsplit=1)
        channels.append(
            Channel(
                id=channel_id,
                device=device,
                name=name,
                channel_type=ChannelType.OUTPUT
            )
        )
    i = 0
    num_channels = len(channels)
    outputs = []
    # Review the list of Channels to Pair Appropriate Channels into an Output
    while i < num_channels:
        i += 1
        if i+1 <= num_channels:
            # If this channel device is the same as the next channel's device
            if channels[i].device == channels[i-1].device:
                # Identify Left and Right Channels
                if "FL" in channels[i].name.upper():
                    outputs.append(Output(
                        left = channels[i],
                        right = channels[i-1]
                    ))
                    i += 1
                    continue
                elif "FR" in channels[i].name.upper():
                    outputs.append(Output(
                        right = channels[i],
                        left = channels[i-1]
                    ))
                    i += 1
                    continue
        # Use Left-Channel Only if there's no left/right
        outputs.append(Output(left=channels[i-1], right=None))
    return outputs


def list_links() -> List[Link]:
    """List the Links."""
    # TODO
    stdout, _ = _execute_shell_command([PW_LINK_COMMAND, "--links", "--id"])
