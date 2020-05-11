# gdc-bot

A Discord bot for a local game development club in Helsinki.

## Commands

```
Helsinki GameDev Club Discord Bot

coin        Flips a coin
dice        Throws a d6 dice
```

## Development

**Step 1**: Clone repository and set up virtual environment.
```
git clone git@github.com:doc97/gdc-bot
# Alternatively, you can use
#   git clone https://github.com/doc97/gdc-bot
# if you do not have SSH keys set up

cd gdc-bot
python -m venv venv
```

**Step 2**: Install dependencies

```
source venv/bin/activate        # On Linux
source venv/Scripts/activate    # On Windows
pip install -r requirements.txt # Install dependencies
```

**Step 3**: Later, make sure venv is activated. If not:
```
source venv/bin/activate        # Activate virtual environment
...                             # Do development work
deactivate                      # Deactivate virtual environment
```

_**Note!** On Windows, use the command `source venv/Scripts/activate`
instead._