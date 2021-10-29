#!/usr/bin/python3
"""VodHelper 0.1"""
import sys
import requests
import time
#import ffmpy -- ffmpy will be used to concatenate actual video data in the future. However, this breaks the Twitch Dev Terms of Service, as web scraping is needed.
#import os
import datetime
import random

def createTStamps(headers, vod_id, id, date, end_date):
  clip_url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&started_at={}&ended_at={}&first=25".format(id, date, end_date)
  clip_req = requests.get(url=clip_url, headers=headers)
  clip_data = clip_req.json()
  clip_list = []
  for item in clip_data['data']: #filters clip data by video id, reduces clutter in console
    if int(item['video_id']) == int(vod_id):
      #print("\n" + str(item)) -- for debug
      vod_time = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
      clip_time = datetime.datetime.strptime(item['created_at'], '%Y-%m-%dT%H:%M:%SZ')
      clip_duration = datetime.datetime.strptime(str(round(item['duration'] - 1)), '%S')
      time_stamp = datetime.datetime.strptime(str(clip_time - vod_time), '%H:%M:%S')
      end_clip = time_stamp - datetime.timedelta(seconds=clip_duration.second) #very messy way of getting the time needed, will fix in the future.
      clip_list.append("{}: {} ------>> {}".format(item['title'], str(end_clip.strftime('%-H:%M:%S')), str(time_stamp.strftime('%-H:%M:%S'))))
  print()
  print("Clip request ended with {}.".format(clip_req.status_code))
  clip_req.close()
  return(clip_list)


def createFile(str_list, stream_title, stream_date):
  with open('{}.txt'.format(stream_title), 'w') as f:
    f.write("-------------------- Clips for '{}'--------------------\n\n".format(stream_title))
    f.write("\n\tStream Date: {}\n\n".format(stream_date.strftime('%Y-%m-%d')))
    f.write("Notation: <title of clip>: <start_time> ------>> <end_time>\nTimestamps directly related to the location the clip is in the VOD.\n\n")
    f.write("\n\t")
    for item in str_list:
      f.write("{}\n\t".format(item))
    f.write("\n--------------------File Created [{}]--------------------\n".format((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')))
    f.write("\n VodHelper Created by ArtisanGray (Eli Greene) ----- https://github.com/ArtisanGray")
    f.write("\nThank you for using my program!")
  f.close()
  return


if __name__ == "__main__":
  clips = []
  answer = ''
  print("Hello! :) Welcome to VodHelper!")
  print("\n------WARNING:------\nVod entries and requests must not exceed 30 days in age, otherwise the request will be refused.")
  time.sleep(2)

  vod_id = input("Copy the VOD ID and paste here: ")
  vod_url = "https://api.twitch.tv/helix/videos?id={}".format(vod_id)

  access_token = "68dk3akg7xccn0r3w6nf2jvckua9lh"
  client_id = "mzqrmsj82dgfkb5fgh1l95t9c6mukj"

  print("Looking for VOD ({})...".format(vod_url))
  headers = {'Client-ID': client_id, 'Authorization': "Bearer " + access_token}
  vod_req = requests.get(url=vod_url, headers=headers)

  if vod_req.status_code == 200:
    print("VOD ({}) found!".format(vod_url))
    vod_data = vod_req.json()
    time.sleep(1)
    now_date = datetime.datetime.now()
    vod_date = datetime.datetime.strptime(vod_data['data'][0]['created_at'],'%Y-%m-%dT%H:%M:%SZ')
    if (now_date - vod_date).days > 30:
      print("VOD is too old!  \n Closing...")
      sys.exit("try again.")
    elif (now_date - vod_date).days <= 30:
      print("Finding clips that match the video ID...")
      user_id = vod_data['data'][0]['user_id']

      tmp = datetime.datetime.strptime(vod_data['data'][0]['duration'], '%Hh%Mm%Ss')
      vod_end = vod_date + datetime.timedelta(hours=tmp.hour, minutes=tmp.minute, seconds=tmp.second)

      clips = createTStamps(headers, vod_id, user_id, vod_data['data'][0]['created_at'], vod_end.strftime('%Y-%m-%dT%H:%M:%SZ'))
      time.sleep(1)
      print("---------------------------------------------------")
      while answer != 'yes' and answer != 'no':
        answer = input("Clips returned by the Twitch API are ordered in popularity.\nWould you like to randomize the data for a more organic result? (yes/no): ")
        if answer == 'yes':
          random.shuffle(clips)
          break
        elif answer == 'no':
          break
        else:
          answer = ''
      stream_title = vod_data['data'][0]['title']
      createFile(clips, stream_title, vod_date)
    vod_req.close()
    time.sleep(1)
    print("File created! Listed under '{}.txt'.".format(stream_title))

  elif vod_req.status_code == 404 or vod_req.status_code == 400:
    time.sleep(2)
    print("\nNot a valid ID or the program couldn't find it.  \n Closing...")
    vod_req.close()
    sys.exit("try again.")
  sys.exit("Have a good day! :)")