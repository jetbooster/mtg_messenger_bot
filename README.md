# mtg_messenger_bot

Simple Facebook messenger listener for posting magic cards into either one-on-one chats or group messages.

**Note!** The bot logs in as you, and posts messages from your account. Currently it will listen for `[[cardname]]` in any groups you are part of. Be careful, as spammy activity could lead to a ban!

## Dependencies
  * python 3
  * fbchat `pip install fbchat` https://github.com/carpedm20/fbchat
  
## Setup
  * ensure you have the dependencies above
  * edit main.py to contain your facebook email
  * create an adjacent file called 'credentials.txt'
    * First line of file: facebook email
    * second line: password
  * Run the bot with `python3 main.py`
  * summon the bot using `[[cardname]]`. It has pretty decent fuzzy match, but it's not a miracle worker!
  
## Acknowledgements
Thanks to XSlicer, and his work on MTG Card Fetcher for reddit, where I pulled some of the regex and logic.https://github.com/XSlicer
