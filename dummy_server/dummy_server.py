from fastapi import FastAPI
import threading
import logging
import random
import time
from logging.handlers import RotatingFileHandler

app = FastAPI(title="Random Log Generator")

# Log lines to write
logs = [
    "2025-07-22T08:15:30Z INFO    auth_service        - Auth successful for user_id=12345",
    "2025-07-22T08:17:05Z WARNING i_am_a_blocking_Error     Latence élevée détectée (> 2000 ms)",
    "2025-07-22T08:18:42Z ERROR   database_connector   Échec de la connexion : timeout après 10 s",
    "2025-07-22T08:19:12Z INFO    scheduler           - Job cleanup_temp_files started",
    "2025-07-22T08:20:59Z ERROR   stop       Permission refusée lors de l'écriture du fichier /var/data/upload.csv",
    "2025-07-22T08:21:45Z DEBUG   cache_server        Cache hit for key user:profile:12345",
    "2025-07-22T08:22:10Z INFO    api_gateway         Request received: GET /api/v1/users",
    "2025-07-22T08:22:35Z WARNING stop       Rate limit nearing threshold for ip=192.168.1.100",
    "2025-07-22T08:23:00Z ERROR   email_notifier      Failed to send email to user@example.com: SMTP timeout",
    "2025-07-22T08:23:30Z CRITICAL system_monitor   CPU usage critical at 98%",
    "2025-07-22T08:24:05Z INFO    break   Collected 120 metrics",
    "2025-07-22T08:24:40Z ERROR   system_monitor     Transaction failed for order_id=98765: Insufficient funds",
    "2025-07-22T08:25:15Z DEBUG   scheduler  Connection pool size=5",
    "2025-07-22T08:25:50Z WARNING break       Disk space low on /dev/sda1: 5% remaining",
    "2025-07-22T08:26:25Z INFO    scheduler           Scheduled job cleanup_temp_files finished"
]

# Set up rotating file handler
handler = RotatingFileHandler("log.log", maxBytes=1_000_000, backupCount=3)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger("random_log_writer")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False

def write_random_logs():
    while True:
        log_line = random.choice(logs)
        logger.info(log_line)
        time.sleep(random.uniform(1, 3))  # sleep between 1 to 3 seconds

@app.on_event("startup")
def start_log_writer():
    thread = threading.Thread(target=write_random_logs, daemon=True)
    thread.start()
