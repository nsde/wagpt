"""Work in progress!
This module extends the functionality of the bot with extra features.
"""

import random
import requests

def get_meme():
    """Returns a meme from reddit."""

    response = requests.get('https://meme-api.com/gimme')
    response.raise_for_status()

    return response.json()['url']

def get_selfie():
    """Returns a random selfie."""

    return random.choice([
        'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2F736x%2F64%2Ff5%2F01%2F64f501db467c44445285591ab8ca8512.jpg&f=1&nofb=1&ipt=263f42436c7a27b1a575057f3608019ed692b0429b71965c26847d01c9827527&ipo=images',
        'https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fi0.kym-cdn.com%2Fentries%2Ficons%2Ffacebook%2F000%2F026%2F152%2Fgigachad.jpg&f=1&nofb=1&ipt=e6356b734ac414e2a0d0af8a05ed833cb43058fe7d433557d8b3aacc28d6b138&ipo=images',
        'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.ytimg.com%2Fvi%2FUx5cQbO_ybw%2Fmaxresdefault.jpg&f=1&nofb=1&ipt=ccc68a09f9d972bbfd25e186b0ba7b3252e242d16e82cd9fbf56000f59d97fab&ipo=images',
    ])
