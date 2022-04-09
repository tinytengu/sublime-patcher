import os

from sublime import (
    get_sublime_path,
    get_sublime_exec_path,
    get_sublime_exec_bak_path,
    get_sublime_version,
    apply_license
)
from patterns import (
    read_patterns,
    has_patterns,
    write_patterns
)

_DIR = os.path.dirname(__file__)
_OS_NAME = "windows" if os.name == "nt" else "linux"


def main():
    # Gathering Sublime Text info
    sublime_dir = get_sublime_path()
    sublime_exec = get_sublime_exec_path()
    sublime_exec_bak = get_sublime_exec_bak_path()

    if not os.path.exists(sublime_exec):
        print("[Error] Unable to locate Sublime Text executable path in {}".format(
            sublime_dir
        ))
        return

    sublime_version = get_sublime_version()

    print("[Sublime Text %s]\nLocation: %s\n" % (
        sublime_version,
        sublime_exec
    ))

    # Loading HEX patterns
    patterns_file = os.path.join(_DIR, "patterns.json")
    print("Loading HEX patterns for Sublime Text... ", end="")
    try:
        patterns = read_patterns(patterns_file)
    except FileNotFoundError:
        print("Failed")
        return
    print("OK")

    if sublime_version not in patterns or (_OS_NAME not in patterns[sublime_version]):
        print("[Error] Patterns for Sublime Text %s (%s) not found" % (
            sublime_version, _OS_NAME
        ))
        return

    _patterns = patterns[sublime_version][_OS_NAME]

    print("Verifying patterns for Sublime Text %s... " % sublime_version, end="")

    with open(sublime_exec, "rb") as file:
        data = file.read()

    if not has_patterns(data, list(_patterns.keys())):
        if has_patterns(data, list(_patterns.values())):
            print("OK")
            print("Sublime Text executable already has patches applied")
            return
        print("Failed")
        return
    print("OK")

    print("Backing up %s... " % sublime_exec, end="")

    try:
        with open(sublime_exec_bak, "wb") as file:
            file.write(data)
    except PermissionError:
        print("Permission denied")
        return
    print("OK")

    print("Patching %s..." % sublime_exec)

    data_new = write_patterns(data, _patterns)

    print("Saving changes... ", end="")
    try:
        with open(sublime_exec, "wb") as file:
            file.write(data_new)
    except PermissionError:
        print("Permission denied")
        return
    print("OK")

    print("Applying license... ", end="")
    apply_license()
    print("OK")

    print("Done.")


if __name__ == '__main__':
    main()
