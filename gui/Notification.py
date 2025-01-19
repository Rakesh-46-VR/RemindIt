import subprocess
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

class Notification:
    """
    ClassName : Notification
    Description : The class is used to send notifications on the Linux UI (Ubuntu).
    """
    def __init__(self):
        pygame.mixer.init()

    def sendNotification(self, title: str, message: str, urgency: str = "normal", icon: str = None, timeout: int = 5000, soundfilepath: str = None):
        """
        Send a notification using `notify-send`.

        :param title: Title of the notification.
        :param message: Message content.
        :param urgency: Urgency level ('low', 'normal', 'critical').
        :param icon: Path to the notification icon (optional).
        :param timeout: Time (in milliseconds) the notification is displayed.
        """
        command = [
            "notify-send",
            title,
            message,
            f"--urgency={urgency}",
            f"--expire-time={timeout}",
        ]
        if icon:
            command.extend(["--icon", icon])

        subprocess.run(command, check=True)

        pygame.mixer.music.load(soundfilepath)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            continue

# Example usage
if __name__ == "__main__":
    notification = Notification()
    notification.sendNotification(
        title="Reminder", 
        message="Time to take a break!", 
        urgency="critical", 
        icon="/home/rakesh/Desktop/Git Hub Projects/RemindIt/logo.png",
        soundfilepath="/home/rakesh/Desktop/Git Hub Projects/RemindIt/Normal.mp3",
        timeout=2000
    )