from pipewire_python.controller import Controller
# import requests


# response=requests.get('https://github.com/pablodz/pipewire_python/blob/main/docs/beers.wav?raw=true')

# with open("beers.wav", 'w') as file:
#     file.write(response.text)

#########################
# PLAYBACK              #
#########################
# normal way
def test_playback():
    audio_controller = Controller(verbose=True)
    audio_controller.set_config(rate=384000,
                                channels=2,
                                _format='f64',
                                volume=0.98,
                                quality=4,
                                # Debug
                                verbose=True)
    audio_controller.playback(audio_filename='docs/beers.wav',
                              # Debug
                              verbose=True)

    assert type(audio_controller.get_config())
