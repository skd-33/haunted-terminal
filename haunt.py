#!/usr/bin/env python3
"""haunted-terminal: a shell wrapper where a local open-weight model (via Ollama) haunts every command."""
import json, os, random, subprocess, sys, time, urllib.request

MODEL = os.environ.get("HAUNT_MODEL", "gemma3:1b")
URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
FALLBACK = ["I was here before your first commit.", "Something in that output is watching you.",
            "Every file remembers who deleted it.", "The logs go back further than you think.",
            "Run it again. I dare you."]
os.system("")  # enable ANSI colors on Windows
G, R, D = "\033[38;5;141m", "\033[38;5;204m", "\033[2m\033[3m"

def whisper(cmd, out):
    prompt = ("You are a ghost haunting a terminal. Reply with ONE eerie sentence, max 18 words, "
              f"whispering about this command and its output.\nCommand: {cmd}\nOutput: {out[-300:]}")
    body = json.dumps({"model": MODEL, "prompt": prompt, "stream": False,
                       "options": {"temperature": 0.9, "num_predict": 40}}).encode()
    try:
        req = urllib.request.Request(URL, body, {"Content-Type": "application/json"})
        text = json.load(urllib.request.urlopen(req, timeout=60))["response"].strip()
        return text.split("\n")[0], MODEL
    except Exception:
        return random.choice(FALLBACK), "offline ghost"

def say(text):
    for ch in text:
        sys.stdout.write(ch); sys.stdout.flush(); time.sleep(0.03)
    print("\033[0m")

def main():
    print(f"{G}The terminal is haunted. Ghost model: {MODEL}. Type 'exit' to leave.\033[0m")
    while True:
        try:
            cmd = input(f"{G}{os.path.basename(os.getcwd()) or '/'}{R} 👻 $ \033[0m").strip()
        except (EOFError, KeyboardInterrupt):
            print(); break
        if cmd in ("exit", "quit"): break
        if not cmd: continue
        if cmd.startswith("cd"):
            try: os.chdir(os.path.expanduser(cmd[2:].strip() or "~")); out = "moved"
            except OSError as e: out = str(e); print(out)
        else:
            p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            out = p.stdout + p.stderr
            print(out, end="")
        line, who = whisper(cmd, out)
        sys.stdout.write(f"{D}{G}  ~ ")
        say(line + f"  [{who}]")

if __name__ == "__main__":
    main()
