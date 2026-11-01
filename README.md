# haunted-terminal

Hacktoberfest Week 4: Ghost in the Machine. A shell wrapper where a local open-weight model haunts every command you run.

## Run
1. Install [Ollama](https://ollama.com) and run `ollama pull gemma3:1b`
2. `python haunt.py` (no dependencies, Python 3.8+)
3. Use another model: `HAUNT_MODEL=qwen2.5:1.5b python haunt.py`

If Ollama isn't running, an offline fallback ghost whispers instead. Everything stays on your machine.

## Web version
`index.html` (my portfolio) has a `haunt` command. It tries your local Ollama from the browser, and falls back to built-in whispers.
