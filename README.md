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
    python -m venv .venv
    .venv/Scripts/activate
    ```
    On Linux / MacOS:
    ```shell
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2. **Install the requirements**
    ```shell
    pip3 install -r requirements.txt
    ```

3. **Run setup.py script**
   
   On Windows:
   ```shell
   python setup.py
   ```
    On Linux / MacOS:
    ```shell
    python3 setup.py
    ```
   And then fill in all the required fields


### ⏯ **To run bot execute with the virtual environment activated:**
```shell
python3 main.py
```