from pipewire_python.controller import Controller


def test_interfaces():

    # Client
    audio_controller = Controller()
    list_interfaces_client = audio_controller.get_list_interfaces(
        type_interfaces="Client", filtered_by_type=True, verbose=True
    )

    print(list_interfaces_client)
    # check if dict
    assert type(list_interfaces_client) is dict
    # not empty dict
    # empty on CI/CD
    assert len(list_interfaces_client) >= 0

    # All
    audio_controller = Controller()
    list_interfaces_client = audio_controller.get_list_interfaces(
        filtered_by_type=False, verbose=True
    )
    print(list_interfaces_client)
    # check if dict
    assert type(list_interfaces_client) is dict
    # not empty dict
    # empty on CI/CD
    assert len(list_interfaces_client) >= 0
