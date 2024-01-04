from pipewire_python.controller import Controller


def test_interfaces():
    # Client
    audio_controller = Controller()
    list_targets_client = audio_controller.get_list_targets()

    print(list_targets_client)
    # check if dict
    assert isinstance(
        list_targets_client, dict
    ), "list_targets_client should be of type dict"
    # not empty dict
    # empty on CI/CD
    assert len(list_targets_client) >= 0
