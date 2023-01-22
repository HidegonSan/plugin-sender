import ftplib
import os
import shutil
import sys

try:
    import dotenv
except ImportError:
    print("Error: dotenv is not installed")
    print("pip3 install python-dotenv")
    sys.exit(1)



def ftp_upload(hostname: str, port: int, upload_src_path: str, upload_dst_path: str, timeout: int) -> bool:
    with ftplib.FTP() as ftp:
        try:
            ftp.connect(host=hostname, port=port, timeout=timeout)
            ftp.set_pasv(True)

            with open(upload_src_path, "rb") as fp:
                ftp.storbinary(upload_dst_path, fp)

        except ftplib.all_errors as e:
            print("FTP error:", e)
            return False

    return True


def main() -> None:
    dotenv.load_dotenv()

    try:
        send_to:         (str | None)  =  os.getenv("SEND_TO")
        as_default:      (str | None)  =  os.getenv("AS_DEFAULT")
        plugin_name:     (str | None)  =  os.getenv("PLUGIN_NAME")
        title_id:        (str | None)  =  os.getenv("TITLE_ID")
        hostname:        (str | None)  =  os.getenv("HOSTNAME")
        citra_sdmc_path: (str | None)  =  os.getenv("CITRA_SDMC_PATH")

        if (any([i is None for i in (send_to, as_default, plugin_name, title_id, hostname, citra_sdmc_path)])):
            raise ValueError("Property is None")

    except Exception:
        print("Error: .env file not found or invalid.")
        sys.exit(1)

    send_to = send_to.casefold()
    plugin_name: str        = plugin_name[2:] if plugin_name.startswith("./") else plugin_name
    citra_sdmc_path: str    = citra_sdmc_path[:-1] if citra_sdmc_path.endswith("/") else citra_sdmc_path
    dst_path: str           = f"/luma/plugins/{title_id}/{plugin_name}"
    port: int               = 5000
    timeout:int             = 500

    if (send_to == "3ds" or send_to == "both"):
        print(f"\n[3ds] Trying to upload {plugin_name} to {hostname + ':' + str(port) + dst_path[5:]}")
        is_upload_successful: bool = ftp_upload(hostname, port, plugin_name, "STOR " + dst_path, timeout)
        print("[3ds] Successfully uploaded!" if is_upload_successful else "[3ds] Upload failed...")

        if (as_default.casefold() == "true"):
            print(f"\n[3ds] Trying to upload {plugin_name} to {hostname + ':' + str(port) + '/luma/plugins/default.3gx'}")
            is_upload_successful: bool = ftp_upload(hostname, port, plugin_name, "STOR /luma/plugins/default.3gx", timeout)
            print("[3ds] Successfully uploaded!" if is_upload_successful else "[3ds] Upload failed...")

    if (send_to == "citra" or send_to == "both"):
        print(f"\n[Citra] Trying to copy {plugin_name} to {citra_sdmc_path + dst_path}")

        try:
            shutil.copyfile(plugin_name, citra_sdmc_path + dst_path)
            print("[Citra] Successfully copied!")
        except Exception:
            print("[Citra] Copy failed...")

        if (as_default.casefold() == "true"):
            print(f"\n[Citra] Trying to copy {plugin_name} to {citra_sdmc_path + '/luma/plugins/default.3gx'}")

            try:
                shutil.copyfile(plugin_name, citra_sdmc_path + "/luma/plugins/default.3gx")
                print("[Citra] Successfully copied!")
            except Exception:
                print("[Citra] Copy failed...")


if __name__ == "__main__":
    main()
    print()


"""
# .env example

# Send type: 3ds, citra, both
SEND_TO="both"

# Send plugin as default.3gx
AS_DEFAULT="true"

# Plugin file name to send
PLUGIN_NAME="./EasyCTRPF.3gx"

# Target title id
TITLE_ID="0004000000155100"

# 3ds hostname
HOSTNAME="192.168.2.100"

# sdmc path of citra
CITRA_SDMC_PATH="/home/hidegon/.var/app/org.citra_emu.citra/data/citra-emu/sdmc/"
"""
