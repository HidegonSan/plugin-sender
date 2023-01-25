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

    # Required
    plugin_name:     (str | None) = os.getenv("PLUGIN_NAME")
    title_id:        (str | None) = os.getenv("TITLE_ID")
    hostname:        (str | None) = os.getenv("HOSTNAME")

    # Optional
    send_to:         str = os.getenv("SEND_TO", default="3ds")
    as_default:      str = os.getenv("AS_DEFAULT", default="false")
    citra_sdmc_path: str = os.getenv("CITRA_SDMC_PATH", default="")

    if (any([i is None for i in (plugin_name, title_id, hostname)])):
        print("Error: .env file not found or invalid.")
        sys.exit(1)

    send_to                 = send_to.casefold()
    plugin_name             = plugin_name[2:] if plugin_name.startswith("./") else plugin_name
    citra_sdmc_path         = citra_sdmc_path[:-1] if citra_sdmc_path.endswith("/") else citra_sdmc_path
    dst_path:           str = f"/luma/plugins/{title_id}/{plugin_name}"
    port:               int = 5000
    timeout:            int = 500

    if (send_to in ("3ds", "both")):
        print(f"\n[3ds Title] Trying to upload {plugin_name} to {hostname + ':' + str(port) + dst_path}")
        is_upload_successful: bool = ftp_upload(hostname, port, plugin_name, "STOR " + dst_path, timeout)
        print("[3ds Title] Successfully uploaded!" if is_upload_successful else "[3ds Title] Upload failed...")

        if (as_default.casefold() == "true"):
            print(f"\n[3ds Default] Trying to upload {plugin_name} to {hostname + ':' + str(port) + '/luma/plugins/default.3gx'}")
            is_upload_successful = ftp_upload(hostname, port, plugin_name, "STOR /luma/plugins/default.3gx", timeout)
            print("[3ds Default] Successfully uploaded!" if is_upload_successful else "[3ds Default] Upload failed...")

    if (send_to in ("citra", "both")):
        print(f"\n[Citra Title] Trying to copy {plugin_name} to {citra_sdmc_path + dst_path}")

        try:
            shutil.copyfile(plugin_name, citra_sdmc_path + dst_path)
            print("[Citra Title] Successfully copied!")
        except Exception:
            print("[Citra Title] Copy failed...")

        if (as_default.casefold() == "true"):
            print(f"\n[Citra Default] Trying to copy {plugin_name} to {citra_sdmc_path + '/luma/plugins/default.3gx'}")

            try:
                shutil.copyfile(plugin_name, citra_sdmc_path + "/luma/plugins/default.3gx")
                print("[Citra Default] Successfully copied!")
            except Exception:
                print("[Citra Default] Copy failed...")


if __name__ == "__main__":
    main()
    print()


"""
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
"""
