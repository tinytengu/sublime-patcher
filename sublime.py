import os
from subprocess import run, PIPE
from binascii import unhexlify


def get_sublime_path() -> str:
    """ Get Sublime Text folder path.

    :return: OS-specific folder path
    :rtype: str
    """
    if os.name == "nt":
        return r"C:\Program Files\Sublime Text"
    return "/opt/sublime_text/"


def get_sublime_exec_path():
    """ Get Sublime Text executable path.

    :return: OS-specific executable path
    :rtype: str
    """
    return os.path.join(
        get_sublime_path(),
        "sublime_text.exe" if os.name == "nt" else "sublime_text"
    )


def get_sublime_exec_bak_path():
    """ Get Sublime Text executable backup path.

    :return: OS-specific executable backup path
    :rtype: str
    """
    return os.path.join(
        get_sublime_path(),
        "sublime_text_bak.exe" if os.name == "nt" else "sublime_text_bak"
    )


def get_license_path() -> str:
    """ Get Sublime Text license file path.

    :return: OS-specific license file path
    :rtype: str
    """
    if os.name == "nt":
        return os.path.join(
            os.getenv("APPDATA"), "Sublime Text", "Local", "License.sublime_license"
        )

    return "/home/$SUDO_USER/.config/sublime-text/Local/License.sublime_license"


def get_sublime_version() -> str:
    """ Get Sublime Text version.

    :return: Sublime Text version
    :rtype: str
    """
    exec_path = get_sublime_exec_path()
    result = run([exec_path, "-v"], stdout=PIPE)
    return result.stdout.decode().strip()[19:]


def apply_license():
    """ Apply Sublime Text license. """
    with open(get_license_path(), "wb") as file:
        file.write(unhexlify(
            b"2d2d2d2d2d20424547494e204c494345"
            b"4e5345202d2d2d2d2d0d0a74696e7974"
            b"656e67750d0a556e6c696d6974656420"
            b"55736572204c6963656e73650d0a4541"
            b"37452d38313034343233300d0a304330"
            b"43443441382043414133313744392043"
            b"43414244314143203433344339383443"
            b"0d0a3745344130423133203737383933"
            b"43334520444430413542413120423245"
            b"42373231430d0a344241414234433420"
            b"39423936343337442031344542373433"
            b"452037444235354439430d0a37434132"
            b"36454532203637433342344543203239"
            b"4232433635412038384439304335390d"
            b"0a434236434342413520374445363137"
            b"37422043303243323832362038433941"
            b"323142300d0a36414231413542362032"
            b"30423039454132203031433937394244"
            b"2032393637304231390d0a3932444336"
            b"44393020364533363538343920344142"
            b"38343733392035423443334541310d0a"
            b"30343843433144302039373438454435"
            b"34204341433944353835203930434144"
            b"3831350d0a2d2d2d2d2d2d20454e4420"
            b"4c4943454e5345202d2d2d2d2d2d"
        ))
