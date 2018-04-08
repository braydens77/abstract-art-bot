# Abstract Art Bot
A bot that generates 2D digital art with color values based on time of day and posts a screenshot of the masterpiece to [Twitter](https://twitter.com/abiotic_art_bot).

## Getting Started
In order to use this art bot, Python 3 is required along with:

* [Twython](https://twython.readthedocs.io/en/latest/) - Twitter API wrapper for Python
* [PyAutoGUI](http://pyautogui.readthedocs.io/en/latest/) - For capturing screenshots

In order to post the images to Twitter, you must [create an app](https://apps.twitter.com) with your Twitter account to generate your authorization tokens.

## Set Up
1. Install Twython and PyAutoGUI
2. Create a Twitter app
3. Generate your Twitter API keys and access tokens
4. Create a file called twitter_credentials.py in the same directory as image_gen.py to store your keys and access tokens

```
CONSUMER_KEY = 'your_key'
CONSUMER_SECRET = 'your_secret'
ACCESS_TOKEN = 'your_token'
ACCESS_TOKEN_SECRET = 'your_token_secret'
```
5. Run with `python image_gen.py`
