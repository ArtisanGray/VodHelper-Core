#!/usr/bin/python3
"""VodHelper 0.1.1"""
import sys
import requests
import time
#import ffmpy -- ffmpy will be used to concatenate actual video data in the future. However, this breaks the Twitch Dev Terms of Service, as web scraping is needed.
#import os
import datetime
import random

def createTStamps(headers, vod_id, id, date, end_date):
  clip_url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&started_at={}&ended_at={}&first=30".format(id, date, end_date)
  #after some testing, it turns out that people dont clip very often during streams. Originally i planned to grab the first 100, but 30 is more consistent in terms of viewership data.
  clip_req = requests.get(url=clip_url, headers=headers)
  clip_data = clip_req.json()
  clip_list = []
  for item in clip_data['data']: #filters clip data by video id, reduces clutter in console
    if int(item['video_id']) == int(vod_id):
      #print("\n" + str(item)) -- for debug
      #It was here that i realized i could've made my own namenclature for the datetime calls.
      vod_time = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
      clip_time = datetime.datetime.strptime(item['created_at'], '%Y-%m-%dT%H:%M:%SZ')
      clip_duration = datetime.datetime.strptime(str(round(item['duration'] - 1)), '%S')
      time_stamp = datetime.datetime.strptime(str(clip_time - vod_time), '%H:%M:%S')
      end_clip = time_stamp - datetime.timedelta(seconds=clip_duration.second) #very messy way of getting the time needed, will fix in the future.
      clip_list.append("{}: {} ------>> {}".format(item['title'], str(end_clip.strftime('%-H:%M:%S')), str(time_stamp.strftime('%-H:%M:%S')))) #appends the timestamp to a list
      #Originally, i was going to do this with a dictionary, but found formatting the strings first then putting it into a list took less lines.
  print()
  print("Clip request ended with {}.".format(clip_req.status_code)) #returns the status code of the request. Pretty inconsequentual, but nice to see anyways.
  clip_req.close()
  return(clip_list)


def createFile(str_list, stream_title, stream_date):
  """Creates the time stamp file."""
  with open('{}.txt'.format(stream_title), 'w') as f: #opens the file needed, named by the grabbed stream title.
  #please forgive the many, many write calls. Im sure there's a way to format multiline but this allows me to change something really quickly if need be.
    f.write("-------------------- Clips for '{}'--------------------\n\n".format(stream_title))
    f.write("\n\tStream Date: {}\n\n".format(stream_date.strftime('%Y-%m-%d')))
    f.write("Notation: <title of clip>: <start_time> ------>> <end_time>\nTimestamps directly related to the location the clip is in the VOD.\n\n")
    f.write("\n\t")
    for item in str_list: #this is responsible for printing the timestamps to file.
      if stream_title not in item:
        f.write("{}\n\t".format(item))
    f.write("\n--------------------File Created [{}]--------------------\n".format((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')))
    f.write("\n VodHelper Created by ArtisanGray (Eli Greene) ----- https://github.com/ArtisanGray")
    f.write("\nThank you for using my program!\n")
  f.close()
  return


if __name__ == "__main__":
  clips = []
  answer = ''
  print("Hello! :) Welcome to VodHelper!")
  print("\n------WARNING:------\nVod entries and requests must not exceed 30 days in age, otherwise the request will be refused.")
  time.sleep(2) #some sleeps are implemented, giving a natural feel to the program.

  vod_id = input("Copy the VOD ID and paste here: ")
  vod_url = "https://api.twitch.tv/helix/videos?id={}".format(vod_id)

  access_token = "68dk3akg7xccn0r3w6nf2jvckua9lh" #Normally you're supposed to hide these, but for this it doesnt matter.
  client_id = "mzqrmsj82dgfkb5fgh1l95t9c6mukj"

  print("Looking for VOD ({})...".format(vod_url))
  headers = {'Client-ID': client_id, 'Authorization': "Bearer " + access_token} #headers to satisfy GET request with - some API features require OAuth authentication.
  vod_req = requests.get(url=vod_url, headers=headers)

  if vod_req.status_code == 200: #If the request was successful, and there's something to return...
    print("VOD ({}) found!".format(vod_url))
    vod_data = vod_req.json()
    time.sleep(1)
    now_date = datetime.datetime.now()
    vod_date = datetime.datetime.strptime(vod_data['data'][0]['created_at'],'%Y-%m-%dT%H:%M:%SZ') #grabs and formats the date associated with the VOD from the API call.
    if (now_date - vod_date).days > 30: #As a safeguard, most accounts are limited to 30 days for archiving their stream VODS. There are exceptions to this, especially if someone is partnered with the platform.
      print("VOD is too old!  \n Closing...")
      sys.exit("try again.") #exits with error message.
    elif (now_date - vod_date).days <= 30:
      print("Finding clips that match the video ID...")
      user_id = vod_data['data'][0]['user_id']

      tmp = datetime.datetime.strptime(vod_data['data'][0]['duration'], '%Hh%Mm%Ss') #temporary variable that is later formatted.
      vod_end = vod_date + datetime.timedelta(hours=tmp.hour, minutes=tmp.minute, seconds=tmp.second)

      clips = createTStamps(headers, vod_id, user_id, vod_data['data'][0]['created_at'], vod_end.strftime('%Y-%m-%dT%H:%M:%SZ')) #obscenely long method call, but it makes sense when you read it. The function returns the list of timestamp data.
      time.sleep(1)
      print("---------------------------------------------------")
      while answer != 'yes' and answer != 'no': #The reason this was put into place was because of the fact that V6 API automatically sorts clips returned by popularity. V5 does not.
        answer = input("Clips returned by the Twitch API are ordered in popularity.\nWould you like to randomize the data for a more organic result? (yes/no): ")
        if answer == 'yes':
          random.shuffle(clips) #this was a breath of relief. I forgot there was a random library on Python.
          break
        elif answer == 'no':
          break
        else:
          answer = ''
      stream_title = vod_data['data'][0]['title']
      createFile(clips, stream_title, vod_date) #sends the timestamp data, stream title and date to be printed to file.
    vod_req.close()
    time.sleep(1)
    print("File created! Listed under '{}.txt'.".format(stream_title))

  elif vod_req.status_code == 404 or vod_req.status_code == 400: #If the request fails...
    time.sleep(2)
    print("\nNot a valid ID or the program couldn't find it.  \n Closing...")
    vod_req.close()
    sys.exit("try again.")
  sys.exit("Have a good day! :)") #Who doesn't like smile faces?
