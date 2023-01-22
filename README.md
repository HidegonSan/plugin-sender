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

# Send type: 3ds, citra, both
SEND_TO=3ds

# Send plugin as default.3gx: true, false
AS_DEFAULT=false

# Plugin file name to send
PLUGIN_NAME=./CTRPF.3gx

# Target title id
TITLE_ID=0004000000155100

# 3ds hostname
HOSTNAME=192.168.2.123

# sdmc path of citra
CITRA_SDMC_PATH=/home/user/.var/app/org.citra_emu.citra/data/citra-emu/sdmc/
```
