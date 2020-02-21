#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import errno

import requests
from bs4 import BeautifulSoup

import re
import argparse
import getpass
import json

def fb_login(email, password):

    if email == None or password == None:
        print 'Login to Facebook:'
        if email == None:
            email = raw_input('Email: ')
        if password == None:
            password = getpass.getpass('Password: ')
    
    s = requests.Session()
    r = s.get('https://www.facebook.com/', allow_redirects=False)
    soup = BeautifulSoup(r.text)
    
    # Handle login form
    action_url = soup.find('form', id='login_form')['action']
    inputs = soup.find('form', id='login_form').findAll('input', {'type': ['hidden', 'submit']})
    post_data = {input.get('name'): input.get('value')  for input in inputs}
    post_data['email'] = email
    post_data['pass'] = password.upper()

    # Find and save the 'datr' cookie
    scripts = soup.findAll('script')
    scripts_string = '/n/'.join([script.text for script in scripts])
    datr_search = re.search('\["_js_datr","([^"]*)"', scripts_string, re.DOTALL)
    if datr_search:
        datr = datr_search.group(1)
        cookies = {'_js_datr' : datr}
    else:
        return False
    s.post(action_url, data=post_data, cookies=cookies, allow_redirects=False)
    return s

def makedirs(path):
    # Create main output directory
    try:
        os.mkdir(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    # Define inner directories
    root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), path)
    messages_dir = os.path.join(root_dir, 'Messages')

    try:
        os.makedirs(messages_dir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def scrape_conversation_list(s,c_user,limit=1000,offset=0):
    """Gets the logged in user's list of conversations, writes to file."""
    people = {}
    convos = []
    
    while(True):
        api_url = "https://www.facebook.com/ajax/mercury/threadlist_info.php?dpr=1&__a=1&__user={}&inbox[limit]={}&inbox[offset]={}".format(c_user,str(limit),offset)
        r = s.get(api_url)

        json_conversation_list = json.loads(r.text[9:])

        try:
            participants = json_conversation_list["payload"]["participants"]
        except KeyError:
            print "Finished scraping {}'s conversation list.".format(c_user)
            break

        try:
            threads = json_conversation_list["payload"]["threads"]
        except KeyError:
            print "Finished scraping {}'s conversation list.".format(c_user)
            break

        for p in participants:
            people[p["fbid"]] = p["name"]
            
        for t in threads:
            c = {}

            # If thread has no fbid, it is a group chat.
            if t["other_user_fbid"] == None:
                c["id"] = t["thread_id"]
                c["name"] = t["name"].encode("utf-8")
            else:
                c["id"] = t["other_user_fbid"]
                c["name"] = people[c["id"]].encode("utf-8")


            convos.append(c)

        offset += limit

    # Backup the list of conversations.
    with open('conversations.txt', 'a+') as f:
        for i,v in enumerate(convos):
            f.write("{} - {} ({})\n".format(i+1,v['name'],v['id']))

    return convos

def scrape_conversation(s,c_user,conv_id,limit=2000):
    """Saves a conversation between the logged in user and a specified other user."""

    if conv_id[:3] == 'id.':
        conv_type = "thread_id"
    else:
        conv_type = "other_user_fbid"

    message_id=None
    direction=None
    messages = ""
    while(True):
        api_url = "https://www.facebook.com/ajax/mercury/search_context.php?dpr=1&__a=1&__user={}&{}={}&limit={}".format(c_user,conv_type,conv_id,str(limit))
        
        if (direction != None):
            api_url += "&direction={}".format(direction)

        if (message_id != None):
            api_url += "&message_id={}".format(message_id)

        print api_url
        r = s.get(api_url)
        json_conversation = json.loads(r.text[9:])


        try:
            new_messages = json_conversation["payload"]["mercury_payload"]["actions"]
        except KeyError:
            print "Finished scraping {}.".format(conv_id)
            break
        
        message_id = new_messages[-1]["message_id"]
        direction = "down"

        messages += json.dumps(new_messages,indent=2)

    return messages
    
def main():
    # Handle command line arguments
    parser = argparse.ArgumentParser(description = 'Create backups of your Facebook conversations.')
    parser.add_argument('--dir', help='specify the output directory')
    parser.add_argument('-u', '--username', help='your facebook username. usually your email address')
    parser.add_argument('-p', '--password', help='your facebook password')
    args = parser.parse_args()

    # Create work directories
    if args.dir == None:
        args.dir = os.path.splitext(os.path.basename(__file__))[0] 
    makedirs(args.dir)
    messages_dir = args.dir + '/Messages/' 

    # Log in
    s = fb_login(args.username, args.password)

    # Find the account's list of conversations.
    conversations = scrape_conversation_list(s,s.cookies["c_user"])

    if len(conversations) == 0:
        print "No conversations found."
    else:
        # Print the account's list of conversations.
        print "The following conversation were found in {}'s account.".format(s.cookies["c_user"])
        for i,v in enumerate(conversations):
            print "{} - {} ({})".format(i+1,v['name'],v['id'])

        # Allow the user to select which conversations to backup.
        print ""
        print "Type numbers of conversations you wish to archive, separated by spaces."
        print "Type 0 to archive all conversations."

        choices = map(int,raw_input("Your choices: ").split()) 

        # Start scraping conversations JSON.
        if choices == [0]:
            print "Scraping all conversations."
            choices = [i+1 for i,v in enumerate(conversations)]
        for i,v in enumerate(choices):
            if v == 0:
                continue
            print "Scraping {}".format(conversations[v-1]["name"])
            messages = scrape_conversation(s,s.cookies["c_user"],conversations[v-1]["id"])

            path = messages_dir + conversations[v-1]["id"]

            try:
                os.makedirs(path)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise

            with open(path + '/conversation.json', 'w+') as f:
                f.write(messages)

if __name__ == "__main__":
    main()
