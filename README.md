# sublime-patcher

Python script for patching/cracking Sublime Text 4 on Windows and Linux.

Unlike the previous Bash script, this implementation supports both Windows and Linux, as well as the easy addition of new Sublime Text builds for cracking process.

![GPL-3.0 License](https://img.shields.io/github/license/tinytengu/sublime-patcher) 

> **Note: Linux**
> 
> This script only works with an *apt* installation of Sublime Text on Linux, *snap* package cannot be supported because of it's read-only structure

> The old Linux bash script has moved to the [bash](https://github.com/tinytengu/sublime-patcher/tree/bash) branch.

## Usage
### Cracking
1. Clone repository
2. Run `main.py` as an administrator on Linux or superuser on Linux
```bash
python3 main.py
```
3. And that's it

<details>
  <summary>Screenshots</summary>
  
  ![Unregistered](https://i.imgur.com/IMOuvhW.png)
  
  ![Process](https://i.imgur.com/9GvdpJJ.png)
  
  ![Registered](https://i.imgur.com/nNZbezS.png)

</details>

### Adding new Sublime Text version to crack
Since this implementation supports an easy way to add new Sublime Text versions as soon as people find the way to crack it, you can contribute and add patches for newer versions in `patterns.json` file which contains HEX patterns to mess with.

Make sure to follow this format:
```json
{
  "sublime_text_build": {
      "windows": {
          "original_hex": "new_hex",
            "original_hex2": "nex_hex2"
        },
        "linux": {
          "original_hex": "new_hex",
            "original_hex2": "new_hex2"
        }
    }
}
```

You can check out [patterns.json](https://github.com/tinytengu/sublime-patcher/blob/main/patterns.json) file to see what it looks like.
