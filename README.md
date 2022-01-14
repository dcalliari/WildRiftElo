# WildRiftElo (Twitch Chat Bot based on BodeDotEXE)
## Setup and Run

Requires Python `3.9`.

Install necessary packages (locally):

```bash
python3 -m pip install -r requirements.txt
```

Copy `.env.sample` to `.env`

```
cp .env.sample .env

```

Open `.env` and insert the following fields:

| Field          | Explanation                                                           |
|----------------|-----------------------------------------------------------------------|
| `TOKEN`        | Access Token obtained from [here](https://twitchtokengenerator.com/)  |
| `BOT_NICK`     | Twitch name of the Bot                                                |
| `BOT_PREFIX`   | Prefix for commands the bot should listen to (set to `!` per default) |

Copy `channels.json.sample` to `channels.json`

```
cp channels.json.sample channels.json

```

Open `channels.json` and follow the instructions:

Start Bot:

```
python3 bot.py
```

## Add the Bot to Autostart/systemd (Raspberry Pi OS)

Install necessary packages (globally):

```bash
sudo -H python3 -m pip install -r requirements.txt
```

Open the unit file [`wildriftelo.service`](./wildriftelo.service) and check if the path to `bot.py` under `[Serivce]` `ExecStart` is correct.

Copy systemd unit file to unit file directory:

```bash
sudo cp wildriftelo.service /lib/systemd/system
```

Reload all units:

```bash
sudo systemctl daemon-release
```

Enable the Twitch Count Bot Unit:

```
sudo systemctl enable wildriftelo.service
```

Start the bot:

```
sudo systemctl start wildriftelo.service
```

Check if the bot is running with:

```
sudo systemctl status wildriftelo.service
```

Check if the output of the bot if an error occurs:

```
sudo systemctl enable wildriftelo.service
```
