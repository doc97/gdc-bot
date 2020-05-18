# gdc-bot

A Discord bot for a local game development club in Helsinki.

## Commands

```
Helsinki GameDev Club Discord Bot 🌈

Commands:
  coin Flips a coin
  dice Throws a d6
Git:
  git  Presents information about various git commands
​No Category:
  help Shows this message

Type !help command for more info on a command.
You can also type !help category for more info on a category.
```

## Setup development

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

## Create your own test bot

1. Visit https://discord.com/developers/ and log in
2. Create a new application
3. Click on the `Bot` menu and create a new bot
4. Switch off the `Public bot` setting
5. Copy the `Token` and paste it in a .env file: `DISCORD_TOKEN=<your-token-here>`
6. Click on the `OAuth2` menu
7. Click on the `bot` checkbox in the scopes section
8. Scroll down and select permissions
9. Copy the generated URL and paste it into the browser
10. Add your bot to a server (you will need to have the `Manage Server` permission to
    add a bot)

## Run tests

Remember to activate your virtual environment before running tests. To run tests,
use:
```
python -m pytest
``` 

Check the [pytest documentation](https://docs.pytest.org/en/latest/index.html) for more details.