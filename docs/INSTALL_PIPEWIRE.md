# PIPEWIRE INSTALLATION

There are several tutorials on the Internet about installing Pipewire. However we recommend this method to avoid errors and unexpected things:

> Disclaimer: Pipewire is under develop, methods may change over time and remember that this software is developed thinking on new distros versions.

## Ubuntu +20.04

1. Uninstall pulseaudio, bluetooth controllers, jack, pavucontrol, and everything based on old (but useful) software:
   1. Run this command to remove pulseaudio:<br>  `sudo apt purge pulseaudio*`
   
   2. Run this command to remove audio control GUI <br> `sudo apt purge pavucontrol*`

   3. Remove other versions of pipewire: <br>`sudo apt purge pipewire*`
   
   4. Remove bluetooth drivers based on pulseaudio and jack applications based on pulseaudio.
   
2. Reboot your computer or laptop
3. Install pipewire via PPA:<br> `sudo add-apt-repository ppa:pipewire-debian/pipewire-upstream` <br> `sudo apt install pipewire`
4. [OPTIONAL] Install `pavucontrol` without pulseaudio: <br>`sudo apt-get install --no-install-recommends pavucontrol`
5. Reboot and change configs in `pavucontrol` to `Pro Audio`

 ![](https://imgur.com/514XIgR.png)
