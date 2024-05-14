# Discord Music Bot

## Overview

`discord-music-bot` is a Discord bot that allows users to play music in their voice channels. It uses Docker for easy deployment and management.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- A Discord bot token. You can create a bot and get the token from the [Discord Developer Portal](https://discord.com/developers/applications).

## Getting Started

### Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/discord-music-bot.git
cd discord-music-bot
```

### Set Up Environment Variables
Create a .env file in the root of the repository and add your Discord bot token:

```bash
DISCORD_TOKEN=your_discord_bot_token
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

### Run the bot
To run the bot, use Docker Compose:

```bash
docker compose up -d
```

### Stopping the Bot
To stop the bot, press CTRL+C in the terminal where docker compose up is running, or run:
```bash
docker compose down
```

# Bot Commands

The `discord-music-bot` provides several commands to manage music playback and other functionalities within a Discord server. Below is a list of the available commands and their descriptions:

## Play Commands

### `!p` or `!play`

**Usage:** `!p <track_name_or_playlist_url>` or `!play <track_name_or_playlist_url>`

**Description:** Plays the specified track or adds a Spotify playlist to the queue. If the bot is not connected to a voice channel, it will join the channel of the user who issued the command.

**Example:**

```bash
!p Never Gonna Give You Up
!play https://open.spotify.com/playlist/...
```

## Queue Commands

### `!queue`

**Usage:** `!queue`

**Description:** Displays the current music queue.

## Playback Control Commands

### `!skip`

**Usage:** `!skip`

**Description:** Skips the currently playing track.

## Follow Commands

### `!follow`

**Usage:** `!follow`

**Description:** Sets the bot to follow the user who issued the command, moving to any voice channel they join.

### `!unfollow`

**Usage:** `!unfollow`

**Description:** Stops the bot from following any user.

## Statistics Command

### `!stats`

**Usage:** `!stats`

**Description:** Displays statistics about the bot's activity, such as the number of tracks played and time spent in voice channels.

## Event Listeners

The bot includes event listeners to handle voice state updates. These listeners are responsible for tracking when members join or leave voice channels, as well as when the bot itself moves.

**Note:** These event listeners are automatically managed by the bot and do not require user interaction.
