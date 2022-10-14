# Discord-Radio

## Need Python 3.10 or higher
## Need Ffmpeg
```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
python main.py
```

### Set discord bot token in ```discord_token.py```

## Discord-Bot commands
\>help - get all available commands

\>info - get all available radio

\>play \<radio name> - play radio. Example: "\>play MyBestRadio"

\>stop - stop radio.

\>volume <int: 0-100> - change volume
