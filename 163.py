import requests
import vlc
import time,threading
import os
from pprint import pprint

version = "0.1"

print("\n  == Cloudmusic Py3 Player (Version "+version+") ==")
print("   |-- Made By Duck1yX64")
print("   |-- Type 'help' for helps.\n")

print("Initializing...")
lastSID = 0
lastSLR = []
lastSLN = ""
vlcMedia = vlc.MediaPlayer()

pstLastID = 0
print("Initializing...Done")

def playST(a):
    global vlcMedia
    global pstLastID
    vlcMedia = vlc.MediaPlayer("https://music.163.com/song/media/outer/url?id="+str(lastSLR[pstLastID])+".mp3")
    vlcMedia.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, playST)
    vlcMedia.play()
    pstLastID = pstLastID + 1

while 1:
    print("\n>> ",end='')
    cmd = input()
    rcmd = cmd.split(' ')

    if cmd == "help":
        print("Helps for Cloudmusic Py3 Player:\n")

        helperary = [
                     "help             Return the manual of Cloudmusic Py3 Player",
                     "devhelp          Return the manual of Cloudmusic Py3 Player for developers",
                     "quit             Quit",
                     "search           Search songs with the keyword,return songs' details",
                     "playlast         Using VLC to play the last song",
                     "checklast        Return the last song's details",
                     "vlc pause        Pause VLC player",
                     "vlc resume       Resume VLC player",
                     "vlc stop         Stop VLC player",
                     "\n*About lists:They're OFFLINE.",
                     "list valid       Check if a songlist is valid",
                     "list load        Load a songlist",
                     "list playlast    Play the last songlist",
                     "list addlast     Add the last song to the last songlist",
                     "list save        Save the songlist data to the last songlist file"
                    ]

        for i in range(len(helperary)):
            print(helperary[i])
            
    elif rcmd[0] == "devhelp":
        if rcmd[1] == 'lastslr':
            print(lastSLR)
        else:
            print("Unknown command.")

    elif cmd == "quit":
        exit()

    elif rcmd[0] == "search":
        tmp_r = requests.get("https://musicapi.leanapp.cn/search?keywords="+cmd[6:])
        tmp_jr = tmp_r.json()

        if tmp_jr['code'] == 200:
            print("Name:"+tmp_jr['result']['songs'][0]['name'])
            print("Artist:"+tmp_jr['result']['songs'][0]['artists'][0]['name'])
            print("ID:"+str(tmp_jr['result']['songs'][0]['id']))
            lastSID = tmp_jr['result']['songs'][0]['id']
        else:
            print("ERROR:Request error "+tmp_jr['code'])

    elif cmd == "playlast":
        if lastSID != 0:
            vlcMedia = vlc.MediaPlayer("https://music.163.com/song/media/outer/url?id="+str(lastSID)+".mp3")
            vlcMedia.play()
            print("Using VLC playing "+str(lastSID)+"...")
        else:
            print("ERROR:Last song ID is 0.")
    
    elif cmd == "checklast":
        if lastSID != 0:
            print("The last song's ID is "+str(lastSID))
        else:
            print("ERROR:Last song ID is 0.")

    elif rcmd[0] == "vlc":
        if rcmd[1] == "pause":
            vlcMedia.pause()
        elif rcmd[1] == "stop":
            vlcMedia.stop()
        elif rcmd[1] == "resume":
            vlcMedia.set_pause(0)
        else:
            print("Unknown command.Please type 'help' for helps.")
    
    elif rcmd[0] == "list":
        if rcmd[1] == "valid":
            if os.path.exists(os.getcwd()+"/"+rcmd[2]+".cppsl"):
                print("Songlist "+rcmd[2]+" exists.")
            else:
                print("Songlist "+rcmd[2]+" doesn't exist.")
        
        elif rcmd[1] == "load":
            if os.path.exists(os.getcwd()+"/"+rcmd[2]+".cppsl"):
                tmp_f = open(os.getcwd()+"/"+rcmd[2]+".cppsl",'r')
                tmp_fd = tmp_f.read()
                lastSLR = []
                lastSLN = rcmd[2]
                for i in range(len(tmp_fd.split(' '))):
                    lastSLR.append(tmp_fd.split(' ')[i])
                tmp_f.close()
                print("Songlist "+rcmd[2]+" is loaded!")
            else:
                print("Songlist "+rcmd[2]+" doesn't exist.")

        elif rcmd[1] == "playlast":
            if len(lastSLR) != 0:
                if vlcMedia.is_playing():
                    vlcMedia.stop()
                print("Start to play the last songlist")
                threading.Thread(target=playST,args=(0,)).start()
            else:
                print("ERROR:Last songlist ID is 0.")

        elif rcmd[1] == "addlast":
            if lastSID != 0:
                lastSLR.append(str(lastSID))
                print("Added the song "+str(lastSID)+" to the last songlist")
            else:
                print("ERROR:The last song's ID is 0.")
                
        elif rcmd[1] == "save":
            tmp_ds = ""
            for i in range(len(lastSLR) - 1):
                tmp_ds = tmp_ds + lastSLR[i] + " "
            tmp_ds = tmp_ds + lastSLR[len(lastSLR) - 1]
            tmp_f = open(os.getcwd()+"/"+lastSLN+".cppsl",'w+')
            tmp_f.write(tmp_ds)
            tmp_f.close()
            print("Saved data to the last songlist "+lastSLN)
        
        else:
            print("Unknown command.Please type 'help' for helps.")

    else:
        print("Unknown command.Please type 'help' for helps.")
