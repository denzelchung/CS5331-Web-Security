#!/usr/bin/python
import sys
import os
import json
import re

# https://developer.chrome.com/extensions/api_index
chrome_apis = ["alarms", "bookmarks", "browsingData", "certificateProvider",
               "contentSettings", "contextMenus", "cookies", "debugger",
               "declarativeContent", "desktopCapture", "documentScan",
               "downloads", "enterprise.deviceAttributes",
               "enterprise.hardwarePlatform", "fileBrowserHandler",
               "fileSystemProvider", "fontSettings", "gcm", "history",
               "identity", "idle", "input", "instanceID", "loginState",
               "management", "networking.config", "notifications",
               "pageCapture", "platformKeys", "power", "printerProvider",
               "printingMetrics", "privacy", "proxy", "sessions",
               "storage", "system.cpu", "system.memory", "system.storage",
               "tabCapture", "tabs", "topSites", "tts", "ttsEngine",
               "vpnProvider", "wallpaper", "webNavigation", "webRequest",
               "permissions.request", "accessibilityFeatures.*.get",
               "accessibilityFeatures.*.set", "accessibilityFeatures.*.clear"]
special_apis = ["document.execCommand\(('|\")paste('|\")\)",
                "document.execCommand\(('|\")copy('|\")\)",
                "document.execCommand\(('|\")cut('|\")\)"]

def main():
    path = sys.argv[1]

    if not os.path.isdir(path):
        if os.path.isfile(path):
            print("{} is a file. Please include the entire directory".format(path))
        else:
            print("{} does not exist.".format(path))
        sys.exit()

    # Extract paths of manifest.json and all js files
    files = []
    manifest = ""
    for (dirpath, dirnames, filenames) in os.walk(path):
        for file in filenames:
            if file.endswith('.js'):
                files.append(os.path.join(dirpath, file))
            if file == 'manifest.json':
                manifest = os.path.join(dirpath, file)

    if manifest == "":
        print("manifest.json is not found")
        sys.exit()

    # Check what API is used in the JavaScript files
    used_apis = set()
    for file in files:
        print("Checking {}...".format(file))
        with open(file, 'r') as fp:
            # read file
            line = fp.readline()
            while line:
                exp = "|".join(["browser."+api for api in chrome_apis]) + "|".join(["chrome."+api for api in chrome_apis])
                regex = re.compile(exp)
                used_apis.update(re.findall(regex, line))

                exp2 = "|".join(special_apis)
                regex2 = re.compile(exp2)
                match = re.search(regex2, line)
                if match:
                    used_apis.add(match.group())
                
                line = fp.readline()

    filtered_permissions = [str.replace(p, "browser.", "") for p in used_apis]
    filtered_permissions = [str.replace(p, "chrome.", "") for p in filtered_permissions]
    used_permissions = set(filtered_permissions)
    print("")
    
    # Check for special cases
    # chrome.instanceID API require gcm permission
    if "instanceID" in used_permissions:
        used_permissions.remove("instanceID")
        used_permissions.add("gcm")

    # chrome.permissions.request - request optional permissions
    if "permissions.request" in used_permissions:
        print("App is using optional permissions")

    # accessibilityFeatures
    to_remove = set()
    addRead = False
    addModify = False
    for p in used_permissions:
        if p.startswith("accessibilityFeatures"):
            if p.endswith("get"):
                addRead = True
            elif p.endswith("set") or p.endswith("clear"):
                addModify = True
            to_remove.add(p)
            
    for r in to_remove:
        used_permissions.discard(r)

    if addRead:
        used_permissions.add("accessibilityFeatures.read")
    if addModify:
        used_permissions.add("accessibilityFeatures.modify")

    # clipboardRead/clipboardWrite
    to_remove = set()
    addClipboardRead = False
    addClipboardWrite = False

    for p in used_permissions:
        if re.match("document.execCommand\(('|\")paste('|\")\)", p):
            addClipboardRead = True
            to_remove.add(p)
        elif re.match("document.execCommand\(('|\")copy('|\")\)", p) or \
             re.match("document.execCommand\(('|\")cut('|\")\)", p):
            addClipboardWrite = True
            to_remove.add(p)

    for r in to_remove:
        used_permissions.discard(r)
    if addClipboardRead:
        used_permissions.add("clipboardRead")
    if addClipboardWrite:
        used_permissions.add("clipboardWrite")
    
    # Check what permissions are declared in manifest.json
    # Check if over declared permissions
    count = 0
    declared_permissions = []
    declared_hosts = []
    with open(manifest, 'r') as json_file:
        data = json.load(json_file)
        for permission in data['permissions']:
            
            # Check hosts
            if re.match("^(http|https|\*)://", permission) or permission == "<all_urls>":
                declared_hosts.append(permission)
                continue
            else:
                declared_permissions.append(permission)
            if permission not in used_permissions:
                if permission not in chrome_apis:
                    print("{} is not capturable by this script.".format(permission))
                else:
                    print("{} is declared but never used".format(permission))
                    count += 1

    # Print results
    print("")
    print("--Results--")
    print("{} permissions are declared but never used.".format(count))
    print("List of permissions used in script: {}".format(", ".join(s for s in used_permissions)))
    print("Declared permissions: {}".format(", ".join(s for s in declared_permissions)))
    print("Declared hosts: {}".format(", ".join(s for s in declared_hosts)))


if __name__ == '__main__':
    main()
