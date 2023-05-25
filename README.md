# `wagpt` (I need a better name xd)
## IMPORTANT QUESTION: Should I separate this project into multiple repositories and one GitHub organization?

There are many different features implemented, and many more are on my list.
We'd have to create a new repository for each feature, and that would make things a bit messy, but at the same time, it could also make things easier to manage.

I'd create the following repositories:
- `/web` - the web UI
- `/ai` - the AI features
- `/extras` - the extra features (searching, memes, etc.)
- `/bridge` - the bridges

***

Unofficial WA Bot powered by OpenAI's GPT models.
Calling it "WA" to prevent legal issues with Meta, but we all know the popular green messaging app.

## Why should I use this?
- Many different features
    - Possibly with the best WhatsApp Selenium bot module

- Widely customizable using `.yml` configuration files
- Well documented `.yml` configuration files

## Limitations
- No API usage, only Selenium -> *slower (can't scale well at all!), not quite unreliable, and certainly most not lightweight*
- ...See the *Bugs* section for more issues that need to be worked on

## Logs
Conversation logs are stored in `conversations/` directory.
They are required for prompting the model.
They don't contain the system prompt, as it changes over time.

You can delete all contents from the `temp/` directory if the bot is not in use, but don't delete the directory itself.

## Usage
Currently, only Windows is supported. We are working on headless Linux support.

1. Install Firefox and geckodriver.
2. Configure the configurations in `.env` (make sure to check out `dotenv-template.txt`) and the files in the `config/` directory.
3. Install the requirements (run in THIS directory!)
```
python -m pip install --upgrade pip
python -m pip install pipreqs
python -m pipreqs.pipreqs . --force
python -m pip install --upgrade -r requirements.txt
```
1. Run the bot: `python wa`.

## Work in progress! Please contribute :)
### Bugs
- [ ] Fix message detection (just because the last detected message has a different ID, doesn't mean it's a new message)
- [ ] Make it work when Windows locked (`pyperclip` issue) - currently using fallback with (possibly) broken emojis
- [ ] Make sure multiple people can use the bot at the same time without any issues (`multithreading`?)
- [ ] Fix `WABot.check_for_message_from_other_chat()` exception:
```py   File "C:\Users\Lynx\Desktop\wagpt\wa\wabot.py", line 69, in check_for_message_from_other_chat
    element.click()
  File "C:\Users\Lynx\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webelement.py", line 94, in click
    self._execute(Command.CLICK_ELEMENT)
  File "C:\Users\Lynx\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webelement.py", line 403, in _execute
    return self._parent.execute(command, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lynx\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py", line 440, in execute
    self.error_handler.check_response(response)
  File "C:\Users\Lynx\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py", line 245, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.ElementClickInterceptedException: Message: Element <div class="_8nE1Y"> is not clickable at point (294,282) because another element <span class="ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr _11JPr"> obscures itStacktrace:
```
- [ ] Make sure messages from users who are not in the contact list of the bot work properly

### General features
- [ ] Easy installer (setup) .exe
- [ ] Web UI

### Browser/WhatsApp client
- [ ] Image support
- [ ] Headless Linux support
- [ ] Change profile picture depending of bot status: online/offline/error

### AI Features
- [ ] Command for clearing one's bot conversation history
- [ ] Meme command
- [ ] Intelligent search support
- [ ] Support for [LibreX Search](https://github.com/hnhx/librex)
- [x] Support for [Whoogle Search](https://github.com/benbusby/whoogle-search)

### Extras
- "Bridges" (send messages from X to WhatsApp and vice versa):
  - [ ] Discord
  - [ ] Telegram

***

## NOT planned right now
Feel free to contribute if you want to implement these features. I don't have the time to do it myself.

- Signal bridge
  - I'd love to, but it's quite hard to do, as Signal is not web-based

- Matrix/IRC/other bridges
    
  - I'd only implement these if we split the project into multiple repositories, as I'd get too cluttered otherwise

- Support for MacOS
    - I don't have a Mac, so I can't test it
    - I don't want to set up a VM just for this

- API support
  - I don't want to create a Facebook account ffs
  - Could get expensive
