# Facebook Chat Backup
Backup your Facebook chats.

## Overview

This utility parses Facebook's JSON serializers for chat information.

Polled API locations:

Account inbox served at https://www.facebook.com/ajax/mercury/threadlist_info.php?dpr=1&__a=1

Conversations served at https://www.facebook.com/ajax/mercury/thread_info.php?dpr=1&__a=1

Note that you need to be logged to access the full functionalities. Faceback can automate this process for you.

## Usage
Faceback.py [-h] [--dir DIR] [-u USERNAME] [-p PASSWORD]

Instructions will appear in the terminal for each stage of the utility's program flow.

First you will be asked to input your Facebook username and password (if they weren't passed as arguments).

If you are logged in succesfully, you will be shown a list of chats found in your Facebook inbox, written in the format:

    ID - NAME (CHAT_ID)
    
At this point you will be prompted to make a selection. You can either:

1. Write a list of space-separated IDs of the chats you wish to archive.
2. Write 0, denoting you wish to archive all chats (this may take a while).

The program ends after all selected chats have been archived.
