# whatsapp-chat-analyze

Command line tool to analyze WhatsApp exported chat data (accepts .txt and .zip) and plot pretty interactive charts.

- [whatsapp-chat-analyze](#whatsapp-chat-analyze)
  - [Demo](#demo)
  - [Features](#features)
  - [Installation](#installation)
    - [pipx](#pipx)
    - [pip](#pip)
  - [Usage](#usage)
  - [Develop](#develop)

## Demo

## Features

- Extracts chat data from .txt or .zip files
- Export to csv (`-c`)

## Installation

### pipx

This is the recommended installation method.

```
$ pipx install whatsapp-chat-analyze
```

### [pip](https://pypi.org/project/whatsapp-chat-analyze/)

```
$ pip install whatsapp-chat-analyze
```

## Usage

```plain
$ whatsapp-chat-analyze --help

usage: whatsapp-chat-analyze [-h] [-n name] [-o base] [-d] [-E] [-c] [-a] file

Analyze Whatsapp Exported .txt or .zip (will be automatically extracted) chat file

positional arguments:
  file                  Chat file (_chat.txt or *.zip) to analyze

options:
  -h, --help            show this help message and exit
  -n name, --chat-name name
                        Name of the chat (default: Chat)
  -o base, --output-base-name base
                        Output base name for the plots (default: whatsapp-chat)
  -d, --by-day-only     Plot messages per day only (default: False)
  -E, --extract-only    Extract the chat and exit (default: False)
  -c, --to-csv-only     Convert chat to csv and exit (default: False)
  -a, --anonymize       Anonymize the chat by replacing author names with generic names (default: False)

```

## Develop

```
$ git clone https://github.com/tddschn/whatsapp-chat-analyze.git
$ cd whatsapp-chat-analyze
$ poetry install
```