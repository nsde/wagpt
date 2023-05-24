# `wagpt`
Unofficial WA Bot powered by OpenAI's GPT models.
Calling it "WA" to prevent legal issues with Meta, but we all know the popular green messaging app.

## Logs
Logs are stored in `logs/` directory.
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

## Features
### Browser/WhatsApp client
- [ ] Image support
- [ ] Headless Linux support

### AI Features
- [ ] Command for clearing one's bot conversation history
- [ ] Meme command
- [ ] Intelligent search support
- [ ] Support for [LibreX Search](https://github.com/hnhx/librex)
- [x] Support for [Whoogle Search](https://github.com/benbusby/whoogle-search)
