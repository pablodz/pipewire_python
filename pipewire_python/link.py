"""
PIPEWIRE's Python controller (wrapper)

Pipewire exposes a command-line interface known as `pw-link` to support linking
between outputs (sources) and inputs (sinks).

```bash
$> pw-link --help
pw-link : PipeWire port and link manager.
Generic: pw-link [options]
  -h, --help                            Show this help
      --version                         Show version
  -r, --remote=NAME                     Remote daemon name
List: pw-link [options] [out-pattern] [in-pattern]
  -o, --output                          List output ports
  -i, --input                           List input ports
  -l, --links                           List links
  -m, --monitor                         Monitor links and ports
  -I, --id                              List IDs
  -v, --verbose                         Verbose port properties
Connect: pw-link [options] output input
  -L, --linger                          Linger (default, unless -m is used)
  -P, --passive                         Passive link
  -p, --props=PROPS                     Properties as JSON object
Disconnect: pw-link -d [options] output input
            pw-link -d [options] link-id
  -d, --disconnect                      Disconnect ports
```


Examples
--------
>>> from pipewire_python import link
>>> inputs = link.list_inputs()
>>> outputs = link.list_outputs()
>>> # Connect the last output to the last input -- during testing it was found
>>> # that Midi channel is normally listed first, so this avoids that.
>>> source = outputs[-1]
>>> sink = inputs[-1]
>>> source.connect(sink)
>>> # Fun Fact! You can connect/disconnect in either order!
>>> sink.disconnect(source) # Tada!
>>> # Default Input/Output links will be made with left-left and right-right
>>> # connections; in other words, a straight stereo connection.
>>> # It's possible to manually cross the lines, however!
>>> source.right.connect(sink.left)
>>> source.left.connect(sink.right)
"""

from typing import List, Union
from dataclasses import dataclass
from enum import Enum

from ._utils import (
    _execute_shell_command,
)

__all__ = [
    "PortType",
    "Port",
    "Input",
    "Output",
    "Link",
    "list_inputs",
    "list_outputs",
    "list_links",
]


PW_LINK_COMMAND = "pw-link"


class InvalidLink(ValueError):
    """Invalid link configuration."""

class PortType(Enum):
    """Pipewire Channel Type - Input or Output."""
    INPUT = 1
    OUTPUT = 2


@dataclass
class Port:
    """
    Pipewire Link Port Object.

    Port for an input or output in Pipewire link. This is the basic, structural
    component for the Python wrapper of Pipewire-link. Ports may be connected by
    links, and Inputs/Outputs consist of one or more of these Port objects
    corresponding to left/right channels.

    Attributes
    ----------
    id:             int
                    Pipewire connector identifier.
    device:         str
                    Pipewire device name.
    name:           str
                    Pipewire device connector name, (typically uses FL or FR).
    port_type:      PortType
                    Designation of connector as input or output.
    is_midi:        bool
                    Indicator to mark that the port is a Midi connection.
    """

    device: str
    name: str
    id: int
    port_type: PortType
    is_midi: bool = False

    def _join_arguments(self, other: "Port", message: str) -> List[str]:
        """Generate a list of arguments to appropriately set output, then input
        for the connection/disconnection command."""
        args = [PW_LINK_COMMAND]
        if self.port_type == PortType.INPUT:
            if other.port_type == PortType.INPUT:
                raise InvalidLink(message.format("input"))
            # Valid -- Append the Output (other) First
            args.append(":".join((other.device, other.name)))
            args.append(":".join((self.device, self.name)))
        else:
            if other.port_type == PortType.OUTPUT:
                raise InvalidLink(message.format("output"))
            # Valid -- Append the Output (self) First
            args.append(":".join((self.device, self.name)))
            args.append(":".join((other.device, other.name)))
        return args

    def connect(self, other: "Port"):
        """Connect this channel to another channel."""
        args = self._join_arguments(
            other=other,
            message="Cannot connect an {} to another {}."
        )
        _ = _execute_shell_command(args)

    def disconnect(self, other: "Port"):
        """Disconnect this channel from another."""
        args = self._join_arguments(
            other=other,
            message="Cannot disconnect an {} from another {}."
        )
        args.append("--disconnect")
        _ = _execute_shell_command(args)

@dataclass
class Input:
    """
    Pipewire Input Object.

    Grouping of left and right channel ports for a Pipewire link input.

    Examples
    --------
    >>> from pipewire_python import link
    >>> inputs = link.list_inputs() # List the inputs on the system.
    >>> # Inputs can also manually built
    >>> my_input = link.Input(
    ...     left = link.Port(
    ...         id=123,
    ...         device="alsa.my.device",
    ...         name="FL",
    ...         port_type=link.PortType.INPUT
    ...     ),
    ...     right = link.Port(
    ...         id=321,
    ...         device="alsa.my.device",
    ...         name="FR",
    ...         port_type=link.PortType.INPUT
    ...     )
    ... )

    Attributes
    ----------
    left:   Port
            Left (or mono) channel port.
    right:  Port
            Right channel port.
    """

    left: Port
    right: Port

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

    Grouping of left and right channel ports for a Pipewire link output.

    Examples
    --------
    >>> from pipewire_python import link
    >>> outputs = link.list_outputs() # List the outputs on the system.
    >>> # Outputs can also manually built
    >>> my_output = link.Output(
    ...     left = link.Port(
    ...         id=123,
    ...         device="alsa.my.device",
    ...         name="FL",
    ...         port_type=link.PortType.OUTPUT
    ...     ),
    ...     right = link.Port(
    ...         id=321,
    ...         device="alsa.my.device",
    ...         name="FR",
    ...         port_type=link.PortType.OUTPUT
    ...     )
    ... )

    Attributes
    ----------
    left:   Port
            Left (or mono) channel port.
    right:  Port
            Right channel port.
    """

    left: Port
    right: Port

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
    """
    List the Inputs Available on System.

    This will identify the available inputs on the system, and proceed with a
    best-effort Input port grouping between left-and-right ports.

    ```bash
    #!/bin/bash
    # Get inputs from output of:
    pw-link --input --id
    ```

    Returns
    -------
    list[Input]:    List of the identified inputs.
    """
    channels = []
    for channel_id, channel_data in _split_id_from_name("--input"):
        device, name = channel_data.split(':', maxsplit=1)
        channels.append(
            Port(
                id=channel_id,
                device=device,
                name=name,
                port_type=PortType.INPUT
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
    """
    List the Outputs Available on System.

    This will identify the available outputs on the system, and proceed with a
    best-effort Output port grouping between left-and-right ports.

    ```bash
    #!/bin/bash
    # Get outputs from output of:
    pw-link --output --id
    ```

    Returns
    -------
    list[Output]:    List of the identified outputs.
    """
    channels = []
    for channel_id, channel_data in _split_id_from_name("--output"):
        device, name = channel_data.split(':', maxsplit=1)
        channels.append(
            Port(
                id=channel_id,
                device=device,
                name=name,
                port_type=PortType.OUTPUT
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
    """
    List the Links Available on System.

    This will identify the present Pipewire links on the system, and proceed
    with a best-effort Link port grouping between left-and-right ports.

    ```bash
    #!/bin/bash
    # Get links from output of:
    pw-link --links --id
    ```

    Returns
    -------
    list[Link]:    List of the identified links.
    """
    # TODO
    stdout, _ = _execute_shell_command([PW_LINK_COMMAND, "--links", "--id"])
