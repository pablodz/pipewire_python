# KNOW ISSUES

1. Multiple "pw-cat" appears on my volume control with `pavucontrol`:
   1. Kill all tasks with pw-cat: <br>
   ```bash
   kill $(pidof pw-play)
   kill $(pidof pw-cat)
   kill $(pidof pw-record)
   ```
   2. All it's ok.