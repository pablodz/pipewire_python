from pipewire_python.controller import Controller

#########################
# PLAYBACK              #
#########################
# normal way


def test_record():
    audio_controller = Controller(verbose=True)
    audio_controller.record(
        audio_filename="1sec_record.wav",
        timeout_seconds=1,
        # Debug
        verbose=True,
    )
    assert type(audio_controller.get_config())
