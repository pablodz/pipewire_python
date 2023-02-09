from pipewire_python.link import (
    list_inputs, list_outputs, list_links, StereoInput, StereoOutput
)


def test_list():
    """Test that the lists provide some devices and that disconnecting clears them."""
    inputs=list_inputs()
    if len(inputs) == 0:
        return # No inputs, no point in testing
    
    assert list_inputs()
    assert list_outputs()

    # Disconnect everything
    for in_dev in list_inputs():
        for out_dev in list_outputs():
            if isinstance(in_dev, StereoInput) and isinstance(out_dev, StereoOutput):
                in_dev.disconnect(out_dev)
    
    assert len(list_links()) == 0

def test_connect_disconnect():
    """Test that all points quickly connect then disconnect."""
    links = []

    # Connect everything
    for in_dev in list_inputs():
        for out_dev in list_outputs():
            if isinstance(in_dev, StereoInput) and isinstance(out_dev, StereoOutput):
                links.append(in_dev.connect(out_dev))
    
    # Disconnect Afterwards
    for link in links:
        link.disconnect()
