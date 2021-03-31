# summarize-bot
Public domain Telegram bot capable of summarizing text and PDF files, as well as answer back with both text and PDF files.

![alt text](https://raw.githubusercontent.com/pabloralves/summarize-bot/master/icon/icon.jpg)

Bot icon made using free software and C0 images.


Based on:
-Telegram bot template by @magnitopic at: https://github.com/magnitopic/YouTubeCode/blob/master/Python/TelegramBots/TelegramBot.py
Thank you!

Capabilities:
- Greets new users
- Answers text with a summary of that text and a brief polite message with the user name.
- Answers PDFs with another PDF containing the same summary. (It assumes PDF is in spanish. If it is in english you must add 'eng' as caption to the file)
- Creates a log of all messages in json format, as well as a local copy of the user sent PDFs, along with the PDF answered, extracted text and text summary.

How to use bot:
1. Connect to botFather on Telegram to get a token and name
2. Insert that token into resumeloBot.py 
3. Run resumeloBot.py to initialize bot
4. Find your bot on Telegram using the name you were given in (1)
5. Interact with bot

Notes:
- All bot messages are in Spanish. Feel free to translate them to your language.
- It is unlikely this project will be maintained in the future
- If using this bot for commercial use, mind the license of the extra modules used: nltk, pdf2image, pytesseract...
