from gui import Notification

notif = Notification()

notif.sendNotification(
    title="Reminder", 
    message="Time to take a break!", 
    urgency="critical", 
    icon="/home/rakesh/Desktop/Git Hub Projects/RemindIt/logo.png",
    soundfilepath="/home/rakesh/Desktop/Git Hub Projects/RemindIt/Normal.mp3",
    timeout=2000
)