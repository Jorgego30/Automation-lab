# 🖥️ Pc Health Bot: 
- A telegram bot designed to monitorizate your pc metrics

## Principal features:
* **Strict identity validation:** Security system that filter ID requests for chat  (`ALLOWED_ID`)
* **Hardware metrics in Real Time:** CPU, RAM and disk storage reports in percentages
* **Alerts:** Messages alerting of too many CPU, RAM use and disk storage.

## Requirements:
* **python-telegram-bot 22.8**
* **python-dotenv 1.2.2**
* **psutil 7.2.2**
* **APScheduler 7.2.2**

## Available commands:
* `/start`: Verifies authentication and welcomes the user.
* `/status`: Returns the percentage of use of CPU, RAM and disks
* `/uptime`: Returns time computer has been turned on
* `/network`: Returns your IP
* `/top_processes`: Returns most expensives processes 
* `/check_thresholds`: Send the alerts of RAM, CPU and disk.

## Stack:
* **Python 3**
* **Ubuntu Linux**
* **Docker**