# Bobabot

## Getting started

Fork and then clone

Navigate into project

```shell
cd bobabot
```
Initialize your python virtual environment

_NOTE_: This is only necessary for new environment setups_

```shell
python -m venv venv
```

Activate the python virtual environment

```shell
source venv/bin/activate
```

Install project dependencies into virtual environment

```shell
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

### Creating a discord bot & server

First, create a new server

Enter server settings

Under Community, register your server as a community server

Add a new forum text channel, make the name match your .env variable *DISCORD_CHANNEL_NAME*

Under the settings for this new channel, add a couple tags. These represent different fields/roles.

```shell
# Example Tags
SWE, PM, DS, UI/UX
```

Additionally, register for a discord developer account and create a new bot application.

Invite your bot to your server with the following set of permissions:

- Manage Server
- Manage Channels
- Send Messages
- Create Public Threads
- Manage Messages
- Embed Links
- Use Slash Commands

_NOTE_: Generate a new token under the *bot* tab and keep it, it will be used later in the .env file


### Docker & MongoDB

Ensure [Docker](https://docs.docker.com/get-docker/) is installed

Open Terminal/Command Prompt

Pull MongoDB

```shell
docker pull mongo:latest
```

Start a mongoDB server bound to port 27017 (Or a port of your choosing, provided you update your localhost address in .env later).

```shell
docker run -d -p 27017:27017 --name bobabot mongo:latest
```

To ensure that our port and container are running properly, in the command prompt write:

```shell
docker ps
```

This should return a list of active containers, and under port you will find listed 0.0.0.0:27017 (or your custom port address)

Next, we need to configure our .env file to ensure we connect to the correct container when running our local development server.

Within your repository, create a file named ".env".

From there copy the contents of sample.env into .env, fill in your own unique token and server, and remove the comments.

### Running Your Test Environment

Start your docker container (If needed) either from the previous guide, or the docker desktop application.

Navigate to your server folder

```shell
cd bobabot/server
```

Run the server with flask

```shell
flask --app routes.py run
```

Open a separate terminal tab and navigate to your bot folder

```shell
cd bobabot/bot
```

From here, run the bot

```shell
python main.py
```

From here, you should see errors and console output within the terminal tab.


### Linting

This project uses [Black](https://github.com/psf/black) as formatting guidelines. [Pre-commit](https://pre-commit.com/) is used to auto format as users commit their work.

```shell
pre-commit run --all-files
```

Run pre-commit on all files to check current formatting status of the project.
