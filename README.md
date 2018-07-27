# mtg_messenger_bot

Simple Facebook messenger listener for posting magic cards into either one-on-one chats or group messages.

**Note!** The bot logs in as you, and posts messages from your account. Currently it will listen for `[[cardname]]` in any groups you are part of. Be careful, as spammy activity could lead to a ban!

## Dependencies
  * python 3
  * fbchat `pip install fbchat` https://github.com/carpedm20/fbchat
  
## Setup
  * ensure you have the dependencies above
  * edit main.py to contain your facebook email
  * run the bot, passing in an environment variable containing your Facebook password
  * Linux/mac(maybe?):
    ```
    MTG_BOT_PASSWORD=password python main.py
    ```
  * Windows:
    ```
    set "MTG_BOT_PASSWORD=password" & python main.py & set "MTG_BOT_PASSWORD=" //remove password from env as soon as possible
    ```
  * summon the bot using `[[cardname]]`. It has pretty decent fuzzy match, but it's not a miracle worker!
