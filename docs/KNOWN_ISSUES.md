# KNOW ISSUES (Ubuntu 20.04+)

- Multiple "pw-cat" appears on my volume control with `pavucontrol`:

   1. Kill all tasks with pw-cat: <br>
   ```bash
   kill $(pidof pw-play)
   kill $(pidof pw-cat)
   kill $(pidof pw-record)
   ```
   2. All it's ok.

- Nothing appears on `pavucontrol (without pulseaudio)`:

   1. Close `pavucontrol`
   
   2. Restart pipewire via `systemctl`:<br>
      ```bash
      #!/bin/bash
      systemctl --user restart pipewire.service
      ```
   
   3. Open `pavucontrol`