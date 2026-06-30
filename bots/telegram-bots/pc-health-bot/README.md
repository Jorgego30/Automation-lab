# 🖥️ Pc Health Bot: 
- A telegram bot designed to monitorizate your pc metrics

## Principal features:
* **Strict identity validation:** Security system that filter ID requests for chat  (`ALLOWED_ID`)
* **Hardware metrics in Real Time:** CPU, RAM and disk storage reports in percentages

## Requirements:
* **python-telegram-bot 22.8**
* **python-dotenv 1.2.2**
* **psutil 7.2.2**

## Installation and Config:
1. **Clone the repository using sparse checkout (only download this project):**
   ```bash
   git clone --no-checkout https://github.com/Jorgego30/Automation-lab.git
   cd Automation-lab
   
   # Initialize sparse-checkout and set the bot folder
   git sparse-checkout init --cone
   git sparse-checkout set Automation_lab/bots/telegram-bots/pc-health-bot
   
   # Download only the configured folder
   git checkout main``` 

2. Go to telegram and search `@bot_father`
3. Send `/start` to `@bot_father` and touch in `/newbot` command
4. Go to telegram and search `@userinfobot`
5. Send `/start` to `@userinfobot` and copy your ID
6. Copy .env.example file and rename it to .env
7. Copy bot token and your ID in .env
8. Launch `python3 pc_health_bot.py`

## Available commands:
* `/start`: Verifies authentication and welcomes the user.
* `/status`: Receive the percentage of use of CPU, RAM and disks

## Stack:
* **Python 3**
* **Ubuntu Linux**