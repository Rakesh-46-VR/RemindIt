from gui import Notification
import os
from dotenv import load_dotenv

load_dotenv()

ICON = os.getenv("ICON")
NORMAL_NOTIFICATION_SOUND = os.getenv("NORMAL_NOTIFICATION_SOUND")

notif = Notification()

notif.sendNotification(
    title="Reminder", 
    message="Time to take a break!", 
    urgency="critical", 
    icon=ICON,
    soundfilepath=NORMAL_NOTIFICATION_SOUND,
    timeout=2000
)