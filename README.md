# BMSTU Parser

---
This project is asynchronous Telegram bot that parses channels of Bauman Moscow State Technical University, finds important posts
and notifies users.

Under the hood, it uses [neural network](https://huggingface.co/HellSoop/BMSTU_parser_model), based on
[XLM-RoBERTa](https://huggingface.co/FacebookAI/xlm-roberta-base) for filtering posts, 
[Pyrogram](https://docs.pyrogram.org/) for parsing Telegram and [requests](https://requests.readthedocs.io/en/latest/)
for parsing VK. Bot is powered by [aiogram](https://aiogram.dev/).

---
## 📜Installation guide
1. **Create and activate a virtual environment**

    On Windows:
    ```shell
    python3 -m venv venv
    venv/Scripts/activate
    ```
    On Linux / MacOS:
    ```shell
    python3 -m venv venv
    source venv/bin/activate
    ```

2. **Install the requirements**
    ```shell
    pip3 install -r requirements.txt
    ```

3. **Fill in the .env file**
   1. **VK_API_TOKEN** as the name suggests, is used for requests to VK (needed for parsing). You can obtain your own token [here](https://id.vk.com/business/go)
   2. **TG_USER_API_ID** and **TG_USER_API_HASH** are Telegram user account data required for parsing Telegram channels. You can obtain it [here](https://core.telegram.org/api/obtaining_api_id)
   3. **BOT_TOKEN** is the authentication token received from [BotFather](https://t.me/BotFather). It's necessary for bot to operate.

4. **Create a database**
    
    Run:
    ```shell
    alembic upgrade head 
    ```

5. **Login to the user's Telegram account**
    
    Run:
    ```shell
    python3 authorize_user_account.py
    ```
   And then fill in all the required fields


### ⏯ **To run bot execute with the virtual environment activated:**
```shell
python3 main.py
```