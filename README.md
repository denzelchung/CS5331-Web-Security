# CS5331-Web-Security

## extensions_fine_grain
This proof of concept uses the **cookies** permission as an example.

_extensions_fine_grain/original_ shows how extension permissions are declared and used with the current Chrome Extension APIs.
_extensions_fine_grain/solution_ gives an idea of how permissions should be broken down into getters and setters.

## extensions_permission_detector
This proof of concept uses _Python 2.7.16_.

_detector.py_ uses keyword matching to identify permissions that an extension require based on the API calls it makes in the source code. Permissions that are declared in _manifest.json_ but not used will be flagged out.

To use: `./detector.py EXTENSION_FOLDER`

List of permissions that are identifiable:
|                             |                              |                    |
|-----------------------------|------------------------------|--------------------|
| alarms                      | bookmarks                    | browsingData       |
| certificateProvider         | contentSettings              | contextMenus       |
| cookies                     | debugger                     | declarativeContent |
| desktopCapture              | documentScan                 | downloads          |
| enterprise.deviceAttributes | enterprise.hardwarePlatform  | fileBrowserHandler |
| fileSystemProvider          | fontSettings                 | gcm                |
| history                     | identity                     | idle               |
| input                       | loginState                   | management         |
| networking.config           | notifications                | pageCapture        |
| platformKeys                | power                        | printerProvider    |
| printingMetrics             | privacy                      | proxy              |
| sessions                    | storage                      | system.cpu         |
| system.memory               | system.storage               | tabCapture         |
| tabs                        | topSites                     | tts                |
| ttsEngine                   | vpnProvider                  | wallpaper          |
| webNavigation               | webRequest                   | gcm                |
| accessibilityFeatures.read  | accessibilityFeatures.modify | clipboardRead      |
| clipboardWrite              | 


Sample output on running the script on the EditThisCookie extension:
![sample output](https://github.com/denzelchung/CS5331-Web-Security/blob/master/extensions_permission_detector/sample-output.png?raw=true "Sample output")
