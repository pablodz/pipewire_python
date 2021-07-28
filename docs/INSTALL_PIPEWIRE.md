# PIPEWIRE INSTALLATION

There are several tutorials on the Internet about installing Pipewire. However we recommend this method to avoid errors and unexpected things:

> Disclaimer: Pipewire is under develop, methods may change over time and remember that this software is developed thinking on new distros versions.

## Ubuntu +20.04

1. Uninstall pulseaudio, bluetooth controllers, jack, pavucontrol, and everything based on old (but useful) software:
   1. Run this command to remove pulseaudio:<br>  `sudo apt purge pulseaudio`
   
   2. [🟡OPTIONAL] Run this command to remove other pulseaudio packages <br> `sudo apt purge gstreamer1.0-pulseaudio libkf5pulseaudioqt-dev libkf5pulseaudioqt2  libkf5pulseaudioqt2-doc liquidsoap-plugin-pulseaudio mkchromecast-pulseaudio osspd-pulseaudio projectm-pulseaudio pulseaudio-dlna pulseaudio-equalizer pulseaudio-esound-compat pulseaudio-module-bluetooth pulseaudio-module-gconf pulseaudio-module-gsettings pulseaudio-module-jacke pulseaudio-module-lirc pulseaudio-module-raop pulseaudio-module-zeroconf pulseaudio-utils squeezelite-pulseaudio  xfce4-pulseaudio-plugin xrdp-pulseaudio-installer -y || echo 'FINISH'`
   
   3. Run this command to remove audio control GUI <br> `sudo apt purge pavucontrol`
   
   4. [🟡OPTIONAL] Run this command to remove other pavucontrol packages <br> `sudo apt purge pavucontrol-qt pavucontrol-qt-l10n`

   5. Remove other versions of pipewire: <br>`sudo apt purge pipewire`
   
   6. [🟡OPTIONAL] Run this command to remove other pipewire and pipewire-pulse packages <br> `sudo apt purge gstreamer1.0-pipewire libpipewire-* pipewire-audio-client-libraries pipewire-*`
   
   7. Remove bluetooth drivers based on pulseaudio and jack applications based on pulseaudio.
   
2. Reboot your computer or laptop
3. Install pipewire via PPA:<br> `sudo add-apt-repository ppa:pipewire-debian/pipewire-upstream` <br> `sudo apt install pipewire`
4. [OPTIONAL] Install `pavucontrol` without pulseaudio: <br>`sudo apt-get install --no-install-recommends pavucontrol`
5. Reboot and change configs in `pavucontrol` to `Pro Audio`

 ![](https://imgur.com/514XIgR.png)
