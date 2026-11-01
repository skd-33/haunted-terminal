# Haunted Terminal

Hacktoberfest Open-Source AI Challenge, Week 4: **Ghost in the Machine**.

A shell wrapper where a ghost whispers about every command you run. After each command, a local open-weight model reads what you ran and replies with one eerie sentence. Everything runs on your own machine.

## What it does

1. You type a command (`ls`, `git status`, anything).
2. `haunt.py` runs it normally and prints the output.
3. It sends the command and the last 300 characters of output to a local model through Ollama.
4. The ghost's reply is typed out under the output, tagged with the model that wrote it.

If Ollama isn't running, an offline fallback ghost whispers instead, so the terminal never breaks.

## Example session

The whisper lines below are an illustration of the format. Real replies vary because the model is creative.

```
project 👻 $ ls
README.md  haunt.py
  ~ Only two files remain. The others never left the directory.  [gemma3:1b]

project 👻 $ cat missing.txt
cat: missing.txt: No such file or directory
  ~ Some files exist only in memory.  [gemma3:1b]
```

## Run it

1. Install [Ollama](https://ollama.com) and pull a model: `ollama pull gemma3:1b`
2. Run `python haunt.py` (Python 3.8+, no packages to install)
3. Type commands. Type `exit` to leave.

Switch models with an environment variable:

```
HAUNT_MODEL=qwen2.5-coder:3b python haunt.py                # bash / WSL
$env:HAUNT_MODEL="qwen2.5-coder:3b"; python haunt.py         # PowerShell
```

Other settings: `OLLAMA_URL` (default `http://localhost:11434/api/generate`).

## How it works

- One file, standard library only: `subprocess` runs commands, `urllib` calls Ollama's local HTTP API.
- The prompt asks for one sentence of at most 18 words, with `temperature 0.9` and `num_predict 40` so replies are short and fast on a laptop.
- `cd` is handled in-process so the working directory carries over between commands.

## Web version

My terminal-style portfolio at https://skd33.tech has a `haunt` command. It turns the page purple and adds a ghost line after each command. It tries a local Ollama model from the browser (this needs `OLLAMA_ORIGINS` set) and falls back to built-in whispers otherwise.

## Why open-source AI

- **Private:** your commands and their output never leave your computer.
- **Offline:** it works with no internet at all.
- **Free to run:** no API key and no per-command cost.
- **Swappable:** change the model with one environment variable.

## Tested with

`gemma3:1b` and `qwen2.5-coder:3b` through Ollama on a Windows PC.

## Limits

Small models sometimes write generic lines. The command runs through your real shell, so only use it where you'd normally run those commands.

Built for the DEV Hacktoberfest challenge. Entering: Best Use of Gemma.
