# plugin-sender
Tools for sending plugins  
Easily send plugins to 3ds and Citra!

# Usage
```bash
python send.py
```

# .env example
```env
# .env example

# Plugin file name to send
PLUGIN_NAME=CTRPF.3gx

# Target title id
TITLE_ID=0004000000155100

# 3ds hostname
HOSTNAME=192.168.2.123

# Send type (Optional): 3ds(default), citra, both
SEND_TO=3ds

# Send plugin as default.3gx (Optional): true, false(default)
AS_DEFAULT=false

# sdmc path of citra (Optional)
CITRA_SDMC_PATH=/home/user/.var/app/org.citra_emu.citra/data/citra-emu/sdmc/
```
