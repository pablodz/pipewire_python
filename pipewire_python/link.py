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

from dataclasses import dataclass
from enum import Enum
from typing import List, Union

from pipewire_python._utils import (
    _execute_shell_command,
)

__all__ = [
    "PortType",
    "Port",
    "Input",
    "Output",
    "StereoInput",
    "StereoOutput",
    "Link",
    "StereoLink",
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
        """
        Generate a list of arguments to appropriately set output, then input
        for the connection/disconnection command.
        """
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

    def connect(self, other: "Port") -> None:
        """Connect this channel to another channel."""
        args = self._join_arguments(other=other, message="Cannot connect an {} to another {}.")
        _ = _execute_shell_command(args)

    def disconnect(self, other: "Port") -> None:
        """Disconnect this channel from another."""
        args = self._join_arguments(other=other, message="Cannot disconnect an {} from another {}.")
        args.append("--disconnect")
        _ = _execute_shell_command(args)


class Input(Port):
    """
    Pipewire Link Input Port Object.

    Input in Pipewire link. Inputs may be composed into left/right channels with
    StereoInput objects.

    Attributes
    ----------
    id:             int
                    Pipewire connector identifier.
    device:         str
                    Pipewire device name.
    name:           str
                    Pipewire device connector name, (typically uses FL or FR).
    port_type:      PortType
                    Designation of connector as an input. Set to PortType.INPUT
    is_midi:        bool
                    Indicator to mark that the port is a Midi connection.
    """


class Output(Port):
    """
    Pipewire Link Output Port Object.

    Output in Pipewire link. Outputs may be composed into left/right channels
    with StereoOutput objects.

    Attributes
    ----------
    id:             int
                    Pipewire connector identifier.
    device:         str
                    Pipewire device name.
    name:           str
                    Pipewire device connector name, (typically uses FL or FR).
    port_type:      PortType
                    Designation of connector as output. Set to PortType.OUTPUT
    is_midi:        bool
                    Indicator to mark that the port is a Midi connection.
    """


@dataclass
class StereoInput:
    """
    Stereo (paired) Pipewire Input Object.

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
    left:   Input
            Left (or mono) channel port.
    right:  Input
            Right channel port.
    """

    left: Input
    right: Input

    def connect(self, other: "StereoOutput") -> Union["StereoLink", "Link", None]:
        """Connect this input to an output."""
        connections = []
        if self.left and other.left:
            self.left.connect(other.left)
            connections.append(Link(input=self.left, output=other.left))
        if self.right and other.right:
            self.right.connect(other.right)
            connections.append(Link(input=self.right, output=other.right))
        if connections:
            if len(connections) > 1:
                return StereoLink(left=connections[0], right=connections[1])
            return connections
        return None

    def disconnect(self, other: Union["StereoOutput", "StereoLink", "Link"]) -> None:
        """Disconnect this input from an output."""
        if self.left and other.left:
            self.left.disconnect(other.left)
        if self.right and other.right:
            self.right.disconnect(other.right)


@dataclass
class StereoOutput:
    """
    Stereo (paired) Pipewire Output Object.

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
    ...     )from
    ... )

    Attributes
    ----------
    left:   Output
            Left (or mono) channel port.
    right:  Output
            Right channel port.
    """

    left: Output
    right: Output

    def connect(self, other: "StereoInput") -> Union["StereoLink", "Link", None]:
        """Connect this input to an output."""
        connections = []
        if self.left and other.left:
            self.left.connect(other.left)
            connections.append(Link(input=other.left, output=self.left))
        if self.right and other.right:
            self.right.connect(other.right)
            connections.append(Link(input=other.right, output=self.right))
        if connections:
            if len(connections) > 1:
                return StereoLink(left=connections[0], right=connections[1])
            return connections
        return None

    def disconnect(self, other: Union["StereoInput", "StereoLink", "Link"]) -> None:
        """Disconnect this input from an output."""
        if self.left and other.left:
            self.left.disconnect(other.left)
        if self.right and other.right:
            self.right.disconnect(other.right)


@dataclass
class Link:
    """
    Pipewire Link Object.

    Configured Pipewire link between an input and output device.

    Attributes
    ----------
    input:  Input
            Pipewire port object acting as input connected with link.
    output: Output
            Pipewire port object acting as output and connected with link.
    """

    input: Input
    output: Output

    def disconnect(self):
        """Disconnect the Link."""
        self.input.disconnect(self.output)

    def reconnect(self):
        """Reconnect the Link if Previously Disconnected."""
        self.input.connect(self.output)


@dataclass
class StereoLink:
    """
    Stereo (paired) Pipewire Linked Object.

    Configured Pipewire link between a pair of input and output devices acting
    as a stereo pair.

    Attributes
    ----------
    left:   Link
            Pipewire link between output and input for left channel.
    right:  Link
            Pipewire link between output and input for right channel.
    """

    left: Link
    right: Link

    def disconnect(self):
        """Disconnect the stereo pair of links."""
        self.left.disconnect()
        self.right.disconnect()

    def reconnect(self):
        """Reconnect the Link Pair if Previously Disconnected."""
        self.left.reconnect()
        self.right.reconnect()


def _split_id_from_data(command) -> List[List[str]]:
    """Helper function to generate a list of channels"""
    stdout, _ = _execute_shell_command([PW_LINK_COMMAND, command, "--id"])
    data_sets = []
    for port in stdout.decode("utf-8").split("\n"):
        ports = port.lstrip().split(" ", maxsplit=1)
        if len(ports) == 2:
            data_sets.append([port.strip(" ") for port in ports])
    return data_sets


def list_inputs(pair_stereo: bool = True) -> List[Union[StereoInput, Input]]:
    """
    List the Inputs Available on System.

    This will identify the available inputs on the system, and proceed with a
    best-effort Input port grouping between left-and-right ports.

    ```bash
    #!/bin/bash
    # Get inputs from output of:
    pw-link --input --id
    ```

    Parameters
    ----------
    pair_stereo:    bool, optional
                    Control to opt for pairing output ports into their
                    corresponding stereo pairs (left/right).

    Returns
    -------
    list[StereoInput | Input]:  List of the identified inputs or stereo input
                                pairs.
    """
    ports = []
    
    inputs=_split_id_from_data("--input")
    if len(inputs) == 0:
        return ports
    
    for channel_id, channel_data in _split_id_from_data("--input"):
        device, name = channel_data.split(":", maxsplit=1)
        ports.append(
            Input(
                id=channel_id,
                device=device,
                name=name,
                port_type=PortType.INPUT,
            )
        )
    if not pair_stereo:
        return ports
    i = 0
    num_ports = len(ports)
    inputs = []
    # Review the list of ports to Pair Appropriate ports into an Input
    while i < num_ports:
        i += 1
        if i + 1 <= num_ports:
            # If this channel device is the same as the next channel's device
            if ports[i].device == ports[i - 1].device:
                # Identify Left and Right ports
                if "FL" in ports[i].name.upper():
                    inputs.append(StereoInput(left=ports[i], right=ports[i - 1]))
                    i += 1
                    continue
                if "FR" in ports[i].name.upper():
                    inputs.append(StereoInput(right=ports[i], left=ports[i - 1]))
                    i += 1
                    continue
        # Use Left-Channel Only if there's no left/right
        inputs.append(ports[i - 1])
    return inputs


def list_outputs(pair_stereo: bool = True) -> List[Union[StereoOutput, Output]]:
    """
    List the Outputs Available on System.

    This will identify the available outputs on the system, and proceed with a
    best-effort Output port grouping between left-and-right ports.

    ```bash
    #!/bin/bash
    # Get outputs from output of:
    pw-link --output --id
    ```

    Parameters
    ----------
    pair_stereo:    bool, optional
                    Control to opt for pairing output ports into their
                    corresponding stereo pairs (left/right).

    Returns
    -------
    list[StereoOutput | Output]:    List of the identified outputs or stereo
                                    output pairs.
    """
    ports = []
    for channel_id, channel_data in _split_id_from_data("--output"):
        device, name = channel_data.split(":", maxsplit=1)
        ports.append(
            Output(
                id=channel_id,
                device=device,
                name=name,
                port_type=PortType.OUTPUT,
            )
        )
    if not pair_stereo:
        return ports
    i = 0
    num_ports = len(ports)
    outputs = []
    # Review the list of ports to Pair Appropriate ports into an Output
    while i < num_ports:
        i += 1
        if i + 1 <= num_ports:
            # If this channel device is the same as the next channel's device
            if ports[i].device == ports[i - 1].device:
                # Identify Left and Right ports
                if "FL" in ports[i].name.upper():
                    outputs.append(StereoOutput(left=ports[i], right=ports[i - 1]))
                    i += 1
                    continue
                if "FR" in ports[i].name.upper():
                    outputs.append(StereoOutput(right=ports[i], left=ports[i - 1]))
                    i += 1
                    continue
        # Use Left-Channel Only if there's no left/right
        outputs.append(ports[i - 1])
    return outputs


def list_links(pair_stereo: bool = True) -> List[Union[StereoLink, Link]]:
    """
    List the Links Available on System.

    This will identify the present Pipewire links on the system, and proceed
    with a best-effort Link port grouping between left-and-right ports.

    ```bash
    #!/bin/bash
    # Get links from output of:
    pw-link --links --id
    ```

    Parameters
    ----------
    pair_stereo:    bool, optional
                    Control to opt for pairing linked ports into their
                    corresponding stereo pairs (left/right).

    Returns
    -------
    list[StereoLink | Link]:    List of the identified links or linked pairs.
    """
    # Parse STDOUT Data for Port Information
    link_data_lines = _split_id_from_data("--links")
    i = 0
    links = []
    while i < (len(link_data_lines) - 1):
        # Determine Direction of Port Link
        direction, side_b_data = link_data_lines[i + 1][1].split(" ", maxsplit=1)
        # Split Side "A" (first) Port Data
        side_a_device, side_a_name = link_data_lines[i][1].split(":")
        side_a_port = Port(
            device=side_a_device,
            name=side_a_name,
            id=link_data_lines[i][0],
            port_type=PortType.INPUT if direction == "|<-" else PortType.OUTPUT,
        )
        # Split Side "B" (second) Port Data
        side_b_id, side_b_data = side_b_data.split(" ", maxsplit=1)
        side_b_device, side_b_name = side_b_data.split(":")
        side_b_port = Port(
            device=side_b_device,
            name=side_b_name,
            id=side_b_id,
            port_type=PortType.OUTPUT if direction == "|<-" else PortType.INPUT,
        )
        i += 2
        if side_a_port.port_type == PortType.INPUT:
            links.append(Link(input=side_a_port, output=side_b_port))
        else:
            links.append(Link(input=side_b_port, output=side_a_port))
    if not pair_stereo:
        return links
    paired_links = []
    found_devices = []
    i = 0
    while i < len(links) - 1:
        i += 1
        if links[i - 1] not in found_devices:
            # Load preferring inputs
            if links[i].input.device == links[i - 1].input.device:
                # record device name to attempt loading output if found again
                found_devices.append(links[i].input.device)
                if "FL" in links[i].input.name.upper():
                    paired_links.append(StereoLink(left=links[i], right=links[i - 1]))
                elif "FR" in links[i].input.name.upper():
                    paired_links.append(StereoLink(left=links[i - 1], right=links[i]))
                i += 1
            else:
                # Fallback
                paired_links.append(links[i - 1])
        else:
            # Load preferring outputs
            if links[i].output.device == links[i - 1].output.device:
                found_devices.append(links[i].output.device)
                if "FL" in links[i].output.name.upper():
                    paired_links.append(StereoLink(left=links[i], right=links[i - 1]))
                elif "FR" in links[i].output.name.upper():
                    paired_links.append(StereoLink(left=links[i - 1], right=links[i]))
                i += 1
            else:
                # Fallback
                paired_links.append(links[i - 1])
    return paired_links
