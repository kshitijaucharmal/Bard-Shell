# Bard Shell

Bard-Shell is a utility that allows you to use Google's Bard AI in the Linux terminal.

## Examples
Check out the [examples](https://github.com/kshitijaucharmal/Bard-Shell/tree/main/examples) folder for some examples.
(*You can also contribute examples)

## Requirements
+ Python 3.x
+ [Neofetch](https://github.com/dylanaraps/neofetch)
+ [Bard-api](https://github.com/dsdanielpark/Bard-API)
+ [Toml](https://pypi.org/project/toml/)

## Installation
To install Bard Shell, simply clone this repository and run the following commands.
```
chmod +x install.sh
./install.sh
```

To get a list of options, run
```
./bard-shell.py -h
```

> You can link the python file to your local bin folder, but somehow its not working for me

## Authentication
> **Warning** Do not expose the `__Secure-1PSID` 
1. Visit https://bard.google.com/
2. F12 for console
3. Session: Application → Cookies → Copy the value of  `__Secure-1PSID` cookie.
4. Store this value in the config file (default location:`~/.config/bardshell/bard.toml`)

Note that while I referred to `__Secure-1PSID` value as an API key for convenience, it is not an officially provided API key. 
Cookie value subject to frequent changes. Verify the value again if an error occurs. Most errors occur when an invalid cookie value is entered. Taken from the [Bard-api](https://github.com/dsdanielpark/Bard-API) GitHub

## Usage
pipe any commands output into bard-shell.py and give a prompt using the `-p` option.

```bash
ls ~ | ./bard-shell.py -p "Summarize the contents of my directory"
```

Use the `-m` or `--modes` flag to provide specific output. The default modes are listed in the example config.

```bash
./bard-shell.py -m content,code
```

Use the `-s` option to view the prompt being sent to bard. (This is going to be much more customizeable in the future)
```bash
./bard-shell.py -s # Show the prompt being sent
```

## Examples
Some examples of how to use Bard-Shell are:
```bash
# For debugging or finding errors quickly
systemctl status swww | ./bard-shell.py -p "Summarize the command output and suggest solutions to any errors"

# For simple uses
ls ~ | ./bard-shell.py -p "Write a simple story based on aliens based on the contents of this directory"

# For Fun!!
ls ~/Downloads | python ~/dox/programming/Python/Bard-Shell/bard-shell.py -p "Write a short story on the contents of the current directory in a class rick and morty way" -m content
```

## Features

+ Can read from stdin
+ Can prompt Bard with the system info
+ Can be used in the terminal

## Contributing

Just fork this repo and add a pull request !!

## License

Bard Shell is released under the [Apache 2.0](https://github.com/kshitijaucharmal/Bard-Shell/blob/main/LICENSE) License.
