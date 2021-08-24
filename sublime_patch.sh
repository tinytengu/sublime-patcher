#!/bin/bash

prompt_yn() {
	def=$2

	# Normalize default answer and prompt
	case $def in
		[yY]) def="y"; read -r -p "${1} [Y/n] " input;;
		[nN]) def="n"; read -r -p "${1} [y/N] " input;;
	esac

	# Echo 1 if yes else 0
	case $input in
		"")
			if [ $def = "y" ]; then
	echo 1
			else
	echo 0
			fi
		;;
		[yY][eE][sS]|[yY]) echo 1;;
		[nN][oO]|[nN]|*) echo 0;;
	esac
}

get_license_path() {
  locations=(
    "/home/$SUDO_USER/.config/sublime-text/Local/"
    "/home/$SUDO_USER/.config/sublime-text-3/Local/"
  )
  for i in "${locations[@]}"; do
    if [ -d "$i" ]; then
      echo "$i/License.sublime_license"
    fi
  done
}

backup() {
	echo "Backing up '${1}' to '${2}'"
	sudo cp "${1}" "${2}"
}

patch() {
	if [ ! -f "$1" ]; then
		echo "Invalid file '$1'"
		exit 1
	fi

	# Patching an executable
	echo "Patching '$1'..."
	sudo sed -i 's/\x55\x41\x57\x41\x56\x41\x55\x41\x54\x53\x48\x81\xEC\x68\x24\x00\x00/\x48\x31\xC0\xC3\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90/g' $1
	sudo sed -i 's/\xE8\xC2\x78\x18\x00/\x90\x90\x90\x90\x90/g' $1
	sudo sed -i 's/\xE8\xA7\x78\x18\x00/\x90\x90\x90\x90\x90/g' $1
	sudo sed -i 's/\x55\x41\x56\x53\x41\x89\xF6\x48\x89\xFD\x6A\x28/\x48\x31\xC0\x48\xFF\xC0\xC3\x90\x90\x90\x90\x90/g' $1

	# Applyting license file
	echo "Applying license..."
	echo "0000000 3277 1f99 de57 c6bb 9361 7c8b bccb ce48 0000020 4c14 12f1 d357 aed4 970b 31a0 90e5 ab79 0000040 2d10 57e0 b31b eaaa bd48 39a9 a0a7 ee78 0000060 3f28 5bf8 9b19 f097 9f43 6b84 d8c2 bb3a 0000100 2e6b 0387 ba4c c7ce e967 6cf0 d5c2 c93a 0000120 5d62 0584 ce4c bad9 e811 6483 c3c5 ab3b 0000140 2c1c 04f1 ce4e b5ca e364 6887 c7c2 bf38 0000160 597a 0787 b84c bbca fa60 1df5 c4c3 b84e 0000200 2818 0294 c73f b6ba 9b60 1a81 c5c6 b94a 0000220 5d1b 12f1 cb48 b5bf 9813 6481 b1a7 ba3e 0000240 2a6e 778c de4f baca e914 1986 c5bf bc33 0000260 2d6e 068c c648 b4d9 ea1f 65f2 c5c6 ab3a 0000300 5e1b 0b82 cd3c bac8 9b06 1df4 c7c1 ca32 0000320 5e6e 0a82 bd4e c7cb fa65 1ef5 c0b6 b833 0000340 2b1e 0394 bd43 c7bb e314 7cf5 c4b5 bd3c 0000360 276b 76f7 c84f b0cc ea63 6c84 b7a7 c84a 0000400 2c1f 068d de42 c1bb 9f14 6880 b0b2 bf2b 0000420 2d68 00f0 c639 c7ce e362 1a84 c1b3 ab49 0000440 2663 06f7 cb43 b3c0 9e06 18f7 b1c5 ce4e 0000460 3f6b 0783 c842 c5c9 e862 1ffd b7bf b949 0000500 5b1b 7094 bb48 c6ba 9b13 7cf1 b3c2 bb48 0000520 5e62 00f2 cc5a c2cc 981f 6afd d8b3 a626 0000540 3277 1299 b03f a3bd 936a 1986 a6c9 ab4e 0000560 3277 1f99 d357 0000566" > $2
	echo "Done."
}

restore() {
	sudo mv "$2" "$1"
	echo "Patches removed."

	if [ -f "$3" ]; then
		sudo rm "$3"
		echo "License file removed."
	fi
}

# Superuser check
if [ ! "$SUDO_USER" ]; then
	echo "Script requires superuser privileges"
	echo "Try using: sudo ${0}"
	exit 1
fi

# Apt installation check
FILE=/opt/sublime_text/sublime_text
if [ ! -f "$FILE" ]; then
	echo "Sublime Text must be an APT package"
	echo "Check out https://www.sublimetext.com/docs/linux_repositories.html#apt"
	exit 1
fi

# Detecting version
BUILD=$(subl --version | sed -E "s/Sublime Text Build ([0-9]+)/\1/")
echo "Sublime Text ($BUILD) detected"

# License file path
LICENSE=$(get_license_path)

# Making backup
BACKUP="${FILE}_backup"
if [ ! -f "$BACKUP" ]; then
	backup "${FILE}" "${BACKUP}"
	patch "$FILE" "$LICENSE"
else
	PS3="Select an option: "

	select opt in "Patch" "Restore from backup"
	do
		if [[ $REPLY == 1 ]]; then
			yn=$(prompt_yn "Backup file '${BACKUP}' already exists. Replace?" "n")
			if [ $yn -eq 1 ]; then
				backup "${FILE}" "${BACKUP}"
			fi

			patch "$FILE" "$LICENSE"
		elif [[ $REPLY == 2 ]]; then
			restore "$FILE" "$BACKUP" "$LICENSE"
		else
			echo "Invalid option."
		fi
		exit 1
	done
fi
