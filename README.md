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

![](https://github.com/cli/cli/assets/45612704/08026ab5-24c0-4ec1-8afe-903d57654e15)

For more plots and interactity, check out the blog post: https://teddysc.me/blog/whatsapp-chat-analyze .

## Features

- Simple to install and use, no cloning involved, supports modern Python versions 
- Extracts chat data from .txt or .zip files
- Export to csv (`-c`)
- Pretty interactive charts with plotly and save them to HTML files
- 6 different plots, see [demo](#demo)
- Anonymize sender names to `A`, `B`, `C`, etc. (`-a`)

## Installation

Python>=3.10 required.

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