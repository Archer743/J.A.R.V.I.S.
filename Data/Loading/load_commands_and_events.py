import os
from termcolor import colored

loaded = 0

def load_commands(client):
    global loaded

    print(colored("===================", "red") + "FOLDERS" + colored("========================", "red"))
    # Loading Folders

    load_folder(client, "chat")
    load_folder(client, "games")
    load_folder(client, "memes&gifs")
    load_folder(client, "moderation")
    load_folder(client, "music")
    load_folder(client, "poll")
    load_folder(client, "weather")
    
    # Nai otdolu vinagi => vzima vsichki komandi, koito sa loadnati
    load_folder(client, "info")

    print(colored("\n- Loaded Folders: ", "magenta") + colored("{}".format(loaded), "green"))

    load_events(client)

    print(colored("\n- Loaded Events: ", "magenta") + colored("{}".format(loaded), "green"))


def load_folder(client, folder : str):
    global loaded
    for filename in os.listdir('./Commands/{}'.format(folder)):
        if filename.endswith('.py'):
            client.load_extension('Commands.{}.{}'.format(folder, filename[:-3]))

    print(colored("- Folder ", "magenta") + colored("{}".format(folder), 'green') + colored(" is loaded!", "magenta"))
    loaded += 1


def load_events(client):
    global loaded
    loaded = 0
    print(colored("===================", "red") + "EVENTS" + colored("=========================", "red"))
    for filename in os.listdir('./Events'):
        if filename.endswith('.py'):
            client.load_extension('Events.{}'.format(filename[:-3]))
            print(colored("- Event ", "magenta") + colored("{}".format(filename[:-3]), 'green') + colored(" is loaded!", "magenta"))
            loaded += 1