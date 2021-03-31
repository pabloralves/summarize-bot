# summarize-bot
Telegram bot capable of summarizing text and PDF files, as well as answer back with both text and PDF files.

Based on:
-Telegram bot template by @magnitopic at: https://github.com/magnitopic/YouTubeCode/blob/master/Python/TelegramBots/TelegramBot.py
Thank you!

Capabilities:
- Answers text with a summary of that text.
- Answers PDFs with another PDF containing the same summary. (It assumes PDF is in spanish. If it is in english you must add 'eng' as caption to the file)
- Creates a log of all messages in json format, as well as a local copy of the user sent PDFs, along with the PDF answered, extracted text and text summary.

How to use bot:
1. Connect to botFather on Telegram to get a token
2. Insert that token into resumeloBot.py 
3. Run resumeloBot.py to initialize bot
