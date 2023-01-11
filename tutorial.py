from pipewire_python.controller import Controller

# import asyncio

#########################
# PLAYBACK              #
#########################
# normal way
audio_controller = Controller(verbose=True)
audio_controller.set_config(
    rate=384000,
    channels=2,
    _format="f64",
    volume=0.98,
    quality=4,
    # Debug
    verbose=True,
)
audio_controller.playback(
    audio_filename="docs/beers.wav",
    # Debug
    verbose=True,
)

# async way
# player = Player()
# asyncio.run(player.play_wav_file_async('docs/beers.wav',
#                                        verbose=True))

#########################
# RECORD                #
#########################

# normal way
audio_controller = Controller(verbose=True)
audio_controller.record(
    audio_filename="docs/5sec_record.wav",
    timeout_seconds=5,
    # Debug
    verbose=True,
)

# async way
# player = Player()
# asyncio.run(player.record_wav_file_async('docs/5sec_record.wav',
#                                          verbose=True))
