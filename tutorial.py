from pipewire_python.pipewirecontroller import Player
import asyncio

#########################
# PLAYBACK              #
#########################
# normal way
player = Player()
player.play_wav_file('docs/beers.wav',
                     verbose=True)

# async way
player = Player()
asyncio.run(player.play_wav_file_async('docs/beers.wav',
                                       verbose=True))

#########################
# RECORD [default=5sec] #
#########################

# normal way
player = Player()
player.record_wav_file('docs/5sec_record.wav',
                       verbose=True)

# async way
player = Player()
asyncio.run(player.record_wav_file_async('docs/5sec_record.wav',
                                         verbose=True))
