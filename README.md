# Bard Shell

Bard-Shell is a utility that allows you to use Google's Bard AI in the Linux terminal.

## Examples
Check out the [examples](https://github.com/kshitijaucharmal/Bard-Shell/tree/main/examples) folder for some examples.
(*You can also contribute examples)

## Requirements
+ Python 3.x
+ [Bard-api](https://github.com/dsdanielpark/Bard-API)
+ [Toml](https://pypi.org/project/toml/)

## Usage
To install Bard Shell, simply clone this repository and run the following commands.
```
chmod +x install.sh
./install.sh
```
## Authentication
> **Warning** Do not expose the `__Secure-1PSID` 
1. Visit https://bard.google.com/
2. F12 for console
3. Session: Application → Cookies → Copy the value of  `__Secure-1PSID` cookie.
4. Store this value in the config file (default location:`~/.config/bardshell/bard.toml`)

Note that while I referred to `__Secure-1PSID` value as an API key for convenience, it is not an officially provided API key. 
Cookie value subject to frequent changes. Verify the value again if an error occurs. Most errors occur when an invalid cookie value is entered. Taken from the [Bard-api](https://github.com/dsdanielpark/Bard-API) GitHub

## Features

+ Can read from stdin
+ Can prompt Bard with the system info
+ Can be used in the terminal

## Contributing

Just fork this repo and add a pull request !!

## License

Bard Shell is released under the [Apache 2.0](https://github.com/kshitijaucharmal/Bard-Shell/blob/main/LICENSE) License.
