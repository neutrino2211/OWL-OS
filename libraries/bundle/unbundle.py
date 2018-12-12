#@owldoc
import zlib
from .FQL import FUnassign, FUnassign2
import sys

'''@
This file contains code for getting all info for an OWL-OS app
@'''

def byteify(s):
    arr = []
    for c in s:
        arr.append(ord(c))
    return bytearray(arr)

def frombits(bits):
    chars = ""
    for b in range(int(len(bits) / 8)):
        byte = bits[b*8:(b+1)*8]
        chars += chr(int(byte,2))
    return chars

'''@
:function `unpackAssets`
Get all assets in an app and return them in dict form
@'''
def unpackAssets(assets):
    a = str(assets)[2:-1]
    assets_dict = {}
    # print(a)
    a = a.replace("\\\\","\\")
    assets = a.split("*")
    for asset in assets:
        cva = asset.split("?")
        assets_dict[cva[1]] = frombits(FUnassign(FUnassign2(cva[0])))
    return assets_dict


'''@
:function `main`
Return vital application info in the tuple (bundle_name,app_name,main_entry_code,assets_dict)
@'''
def main(args):

    bundle = zlib.decompress(args[0])
    bundle = str(bundle)[2:-1]
    bundle_parts = bundle.split("*")

    # HEADER
    bundle_header = bundle_parts[0]
    bundle_header_content = frombits(FUnassign(FUnassign2(bundle_header.split("?")[0])))

    # Assets
    bundle_assets = bundle_parts[1]
    bundle_assets_content = frombits(FUnassign(FUnassign2(bundle_assets.split("?")[0])))
    assets = unpackAssets(zlib.decompress(byteify(bundle_assets_content)))
    # print(assets)
    if bundle_header_content[:4] == "xOWL":
        app_entry = zlib.decompress(byteify(bundle_header_content[0xf4:]))
        app_header = bundle_header_content[:0xf4]
        app_name,app_package = (app_header[124:].replace("\x00",""),app_header[4:124].replace("\x00",""))
        # print(app_name,app_package)
        return (app_name,app_package,app_entry,assets)
    else:
        print("Error: '{}' is not an owl app".format(args[0]))
        exit(0)

if __name__ == "__main__":
    args = sys.argv[1:]
    content = open(args[0],"rb").read()
    print(main([content]))