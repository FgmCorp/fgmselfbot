# -*- coding: utf-8 -*-
from linepy import *
from liff.ttypes import LiffChatContext, LiffContext, LiffSquareChatContext, LiffNoneContext, LiffViewRequest
from datetime import datetime
import ast, codecs, json, os, re, random, requests, sys, time, traceback

"""
SIMPLE SELFBOT BY FGM CORP: HANSEN & UNYPASS
Special Thanks: HelloWorld & BE-TEAM

Ⓒ FGM CORP 2020
"""
# PLEASE DONT REMOVE CREATOR NAME :)

try:
    FGM = LINE(appName="CHROMEOS\t2.3.8\tChrome_OS\t1")
except Exception as e:
    os.remove("token.json")
    sys.exit("[FGM SERVICE] BOT SHUTDOWN")

print("Need Help?? Join Our Community\nhttps://hansengianto.gq/square.html")

FGMMID = FGM.profile.mid
FGMStart = time.time()
FGMPoll = OEPoll(FGM)
#=======================================
read = {"readMember": {}, "readPoint": {}}
settings = {"changeGroupPicture": [], "changePictureProfile": False}
#=======================================
def restartBot():
    print ("[FGM SERVICE] BOT RESETTED")
    python = sys.executable
    os.execl(python, python, *sys.argv)

def logError(text):
    FGM.log("[ ERROR ] {}".format(str(text)))

def timeChange(secs):
    mins, secs = divmod(secs,60)
    hours, mins = divmod(mins,60)
    days, hours = divmod(hours,24)
    weeks, days = divmod(days,7)
    months, weeks = divmod(weeks,4)
    text = ""
    if months != 0: text += "%02d Bulan" % (months)
    if weeks != 0: text += " %02d Minggu" % (weeks)
    if days != 0: text += " %02d Hari" % (days)
    if hours !=  0: text +=  " %02d Jam" % (hours)
    if mins != 0: text += " %02d Menit" % (mins)
    if secs != 0: text += " %02d Detik" % (secs)
    if text[0] == " ":
        text = text[1:]
    return text

def getMidMentionV2(content, text):
    try:
        if 'MENTION' in content.keys()!= None:
            names = re.findall(r'@(\w+)', text)
            mention = ast.literal_eval(content['MENTION'])
            mentionees = mention['MENTIONEES']
            hasil = []
            for isi in mentionees:
                if isi not in hasil:
                    hasil.append(isi["M"])
            return hasil
        else:
            return []
    except:
        pass

def menuHelp():
    cmdlist = [
        "profile",
        "group",
        "broadcast",
        "tagall",
        "ciduk on/off",
        "ciduk",
        "speed",
        "runtime",
        "restart",
        "logout"
    ]
    isi  = "「 FGM SelfBot 」"
    isi += "\nType: Help"
    for waw in cmdlist:
        isi += "\n➣ "+waw.title()
    isi += "\n\n⌬ Selfbot Ver 0.1"
    isi += "\nⒸ FGM CORP 2020"
    isi += "\n\n「 FGM Community 」"
    isi += "\nhttps://hansengianto.gq/square.html"
    return isi

def menuProfile():
    cmdlist = [
        "me",
        "myprofile",
        "mymid",
        "myname",
        "mybio",
        "mypicture",
        "myvideo",
        "mycover",
        "mid @",
        "name @",
        "bio @",
        "picture @",
        "cover @",
        "updatename [name]",
        "updatebio [bio]",
        "updatedp"
    ]
    isi  = "「 FGM SelfBot 」"
    isi += "\nType: Profile"
    for waw in cmdlist:
        isi += "\n➣ "+waw.title()
    isi += "\n\n⌬ Selfbot Ver 0.1"
    isi += "\nⒸ FGM CORP 2020"
    isi += "\n\n「 FGM Community 」"
    isi += "\nhttps://hansengianto.gq/square.html"
    return isi

def menuGroup():
    cmdlist = [
        "groupname [name]",
        "groupdp",
        "openqr",
        "closeqr",
        "grouplist",
        "groupinfo",
    ]
    isi  = "「 FGM SelfBot 」"
    isi += "\nType: Group"
    for waw in cmdlist:
        isi += "\n➣ "+waw.title()
    isi += "\n\n⌬ Selfbot Ver 0.1"
    isi += "\nⒸ FGM CORP 2020"
    isi += "\n\n「 FGM Community 」"
    isi += "\nhttps://hansengianto.gq/square.html"
    return isi

def menuBroadcast():
    cmdlist = [
        "gbroadcast [message]",
        "fbroadcast [message]"
    ]
    isi  = "「 FGM SelfBot 」"
    isi += "\nType: Broadcast"
    for waw in cmdlist:
        isi += "\n➣ "+waw.title()
    isi += "\n\n⌬ Selfbot Ver 0.1"
    isi += "\nⒸ FGM CORP 2020"
    isi += "\n\n「 FGM Community 」"
    isi += "\nhttps://hansengianto.gq/square.html"
    return isi

def FGMBot(op):
    try:
            if op.type == 25:
                msg = op.message
                text = str(msg.text)
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                cmd = text.lower()
                if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                    if msg.toType == 0:
                        if sender != FGM.profile.mid:
                            to = sender
                        else:
                            to = receiver
                    elif msg.toType == 1:
                        to = receiver
                    elif msg.toType == 2:
                        to = receiver
                    if msg.contentType == 0:
                        if text is None:
                            return
                        #===============
                        # MENU COMMAND
                        #===============

                        elif cmd == "help":
                            helpMessage = menuHelp()
                            FGM.sendMessage(to, helpMessage)

                        elif cmd == "profile":
                            helpMessage = menuProfile()
                            FGM.sendMessage(to, helpMessage)

                        elif cmd == "group":
                            helpMessage = menuGroup()
                            FGM.sendMessage(to, helpMessage)

                        elif cmd == "broadcast":
                            helpMessage = menuBroadcast()
                            FGM.sendMessage(to, helpMessage)

                        elif cmd == 'tagall':
                            group = FGM.getGroup(to)
                            midMembers = [contact.mid for contact in group.members]
                            midSelect = len(midMembers)//20
                            for mentionMembers in range(midSelect+1):
                                no = 0
                                ret_ = "╭━「 FGM SelfBot 」"
                                dataMid = []
                                for dataMention in group.members[mentionMembers*20 : (mentionMembers+1)*20]:
                                    dataMid.append(dataMention.mid)
                                    no += 1
                                    ret_ += "\n┃ {}. @!".format(str(no))
                                ret_ += "\n╰━「 Total {} Members 」".format(str(len(dataMid)))
                                ret_ += "\n\n「 FGM Community 」"
                                ret_ += "\nhttps://hansengianto.gq/square.html"
                                #if dataMid != []:
                                FGM.sendMentionV2(to, ret_, dataMid, isUnicode=True)

                        elif cmd == "ciduk on":
                            if to in read['readPoint']:
                                try:
                                    del read['readPoint'][to]
                                    del read['readMember'][to]
                                except:
                                    pass
                                read['readPoint'][to] = msg_id
                                read['readMember'][to] = []
                                FGM.sendMessage(to, "Lurking telah diaktifkan")
                            else:
                                try:
                                    del read['readPoint'][to]
                                    del read['readMember'][to]
                                except:
                                    pass
                                read['readPoint'][to] = msg_id
                                read['readMember'][to] = []
                                FGM.sendMessage(to, "Set reading point. Type ciduk to see reader")

                        elif cmd == "ciduk off":
                            if to not in read['readPoint']:
                                FGM.sendMessage(to,"Lurking telah dinonaktifkan")
                            else:
                                try:
                                    del read['readPoint'][to]
                                    del read['readMember'][to]
                                except:
                                    pass
                                FGM.sendMessage(to, "Delete reading point")

                        elif cmd == "ciduk":
                            if to in read['readPoint']:
                                if read["readMember"][to] == []:
                                    return FGM.sendMessage(to, "Tidak Ada Sider")
                                else:
                                    midMembers = read["readMember"][to]
                                    midSelect = len(midMembers)//20
                                    for mentionMembers in range(midSelect+1):
                                        no = 0
                                        ret_ = "╭━「 Reader 」"
                                        dataMid = []
                                        for dataMention in midMembers[mentionMembers*100 : (mentionMembers+1)*100]:
                                            dataMid.append(dataMention)
                                            no += 1
                                            ret_ += "\n┃ {}. @!".format(str(no))
                                        ret_ += "\n╰━「 Total {} Members 」".format(str(len(dataMid)))
                                        if dataMid != []:
                                            FGM.sendMentionV2(to, result, read["readMember"][to])
                                    read['readMember'][to] = []

                        elif cmd == "speed":
                            FGM.sendMessage(to, "Counting...")
                            start = time.time()
                            time.sleep(0.006)
                            elapsed_time = time.time() - start
                            FGM.sendMessage(to, "Result: {} Seconds".format(str(elapsed_time)))

                        elif cmd == "runtime":
                            timeNow = time.time()
                            runtime = timeNow - FGMStart
                            runtime = timeChange(runtime)
                            FGM.sendMessage(to, "Active Time: {}".format(str(runtime)))

                        elif cmd == "restart":
                            FGM.sendMessage(to, "Success restart selfbot")
                            restartBot()

                        elif cmd == "logout":
                            FGM.sendMessage(to, "Success disable selfbot")
                            sys.exit("[FGM SERVICE] BOT SHUTDOWN")
                            return

                        #===============
                        # PROFILE COMMAND
                        #===============
                        elif cmd == "me":
                            FGM.sendContact(to, sender)

                        elif cmd == "myprofile":
                            contact = FGM.getContact(sender)
                            cover = FGM.getProfileCoverURL(sender)
                            result = "「 Display Name 」"
                            result += "\n{}".format(contact.displayName)
                            result += "\n\n「 MID 」"
                            result += "\n{}".format(contact.mid)
                            result += "\n\n「 Status Message 」"
                            result += "\n{}".format(contact.statusMessage)
                            if contact.pictureStatus != None:
                                FGM.sendImageWithURL(to, "https://obs.line-scdn.net/{}".format(contact.pictureStatus))
                            FGM.sendMentionV2(to, result, [sender])

                        elif cmd == "mymid":
                            contact = FGM.getContact(sender)
                            FGM.sendMessage(to, sender)

                        elif cmd == "myname":
                            contact = FGM.getContact(sender)
                            FGM.sendMessage(to, contact.displayName)

                        elif cmd == "mybio":
                            contact = FGM.getContact(sender)
                            FGM.sendMessage(to, contact.statusMessage)

                        elif cmd == "mypicture":
                            contact = FGM.getContact(sender)
                            FGM.sendImageWithURL(to, "https://obs.line-scdn.net/{}".format(contact.pictureStatus))

                        elif cmd == "myvideo":
                            contact = FGM.getContact(sender)
                            if contact.videoProfile == None:
                                return FGM.sendMessage(to, "Anda tidak memiliki video profile")
                            else:FGM.sendVideoWithURL(to, "https://obs.line-scdn.net/{}/vp".format(contact.pictureStatus))

                        elif cmd == "mycover":
                            cover = FGM.getProfileCoverURL(sender)
                            FGM.sendImageWithURL(to, str(cover))

                        # STEAL PROFILE

                        elif cmd.startswith("mid "):
                            ls = getMidMentionV2(msg.contentMetadata, text)
                            for ls in lists:
                                FGM.sendMessage(to, ls)

                        elif cmd.startswith("name "):
                            ls = getMidMentionV2(msg.contentMetadata, text)
                            for ls in lists:
                                contact = FGM.getContact(ls)
                                FGM.sendMessage(to, contact.displayName)

                        elif cmd.startswith("bio "):
                            ls = getMidMentionV2(msg.contentMetadata, text)
                            for ls in lists:
                                contact = FGM.getContact(ls)
                                FGM.sendMentionV2(to, "@!: {}".format(contact.statusMessage), [ls])

                        elif cmd.startswith("picture "):
                            ls = getMidMentionV2(msg.contentMetadata, text)
                            for ls in lists:
                                contact = FGM.getContact(ls)
                                FGM.sendImageWithURL(to, "https://obs.line-scdn.net/{}".format(contact.pictureStatus))

                        elif cmd.startswith("cover "):
                            ls = getMidMentionV2(msg.contentMetadata, text)
                            for ls in lists:
                                cover = FGM.getProfileCoverURL(ls)
                                FGM.sendImageWithURL(to, str(cover))

                        # UPDATE PROFILE

                        elif cmd.startswith("updatename "):
                            sep = text.split(" ")
                            name = text.replace(sep[0] + " ","")
                            if len(name) <= 20:
                                profile = FGM.getProfile()
                                profile.displayName = name
                                FGM.updateProfile(profile)
                                FGM.sendMessage(to, "Berhasil mengubah nama menjadi : {}".format(name))

                        elif cmd.startswith("updatebio "):
                            sep = text.split(" ")
                            bio = text.replace(sep[0] + " ","")
                            if len(bio) <= 500:
                                profile = FGM.getProfile()
                                profile.displayName = bio
                                FGM.updateProfile(profile)
                                FGM.sendMessage(to, "Berhasil mengubah bio menjadi : {}".format(bio))

                        elif cmd == "updatedp":
                            settings["changePictureProfile"] = True
                            FGM.sendMessage(to, "Silahkan kirim gambarnya")

                        #===============
                        # GROUP COMMAND
                        #===============

                        elif cmd.startswith("groupname "):
                            if msg.toType == 2:
                                sep = text.split(" ")
                                groupname = text.replace(sep[0] + " ","")
                                if len(groupname) <= 20:
                                    group = FGM.getGroup(to)
                                    group.name = groupname
                                    FGM.updateGroup(group)
                                    FGM.sendMessage(to, "Berhasil mengubah nama group menjadi : {}".format(groupname))

                        elif cmd == "groupdp":
                            if msg.toType == 2:
                                if to not in settings["changeGroupPicture"]:
                                    settings["changeGroupPicture"].append(to)
                                FGM.sendMessage(to, "Silahkan kirim gambarnya")

                        elif cmd == "openqr":
                            if msg.toType == 2:
                                group = FGM.getGroup(to)
                                group.preventedJoinByTicket = False
                                FGM.updateGroup(group)
                                groupUrl = FGM.reissueGroupTicket(to)
                                FGM.sendMessage(to, "Berhasil membuka QR Group\n\nGroupURL : line://ti/g/{}".format(groupUrl))

                        elif cmd == "closeqr":
                            if msg.toType == 2:
                                group = FGM.getGroup(to)
                                group.preventedJoinByTicket = True
                                FGM.updateGroup(group)
                                FGM.sendMessage(to, "Berhasil menutup QR Group")

                        elif cmd == "grouplist":
                            groups = FGM.getGroupIdsJoined()
                            ret_ = "╭─[ Group List ]"
                            no = 0
                            for gid in groups:
                                group = FGM.getGroup(gid)
                                no += 1
                                ret_ += "\n➣ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            ret_ += "\n╰─[ Total {} Groups ]".format(str(len(groups)))
                            FGM.sendMessage(to, str(ret_))

                        elif cmd == "groupinfo":
                            group = FGM.getGroup(to)
                            try:
                                try:
                                    groupCreator = group.creator.mid
                                except:
                                    groupCreator = "Tidak ditemukan"
                                if group.invitee is None:
                                    groupPending = "0"
                                else:
                                    groupPending = str(len(group.invitee))
                                if group.preventedJoinByTicket == True:
                                    groupQr = "Tertutup"
                                    groupTicket = "Tidak ada"
                                else:
                                    groupQr = "Terbuka"
                                    groupTicket = "https://line.me/R/ti/g/{}".format(str(FGM.reissueGroupTicket(group.id)))
                                ret_ = "「 Group Info 」"
                                ret_ += "\n➣ Name : {}".format(group.name)
                                ret_ += "\n➣ ID : {}".format(group.id)
                                ret_ += "\n➣ Member : {}".format(str(len(group.members)))
                                ret_ += "\n➣ Pending : {}".format(groupPending)
                                ret_ += "\n➣ Group Qr : {}".format(groupQr)
                                ret_ += "\n➣ Group Ticket : {}".format(groupTicket)
                                FGM.sendImageWithURL(to, "https://obs.line-scdn.net/{}".format(group.pictureStatus))
                                FGM.sendMessage(to, str(ret_))
                                FGM.sendContact(to, groupCreator)
                            except Exception as e:
                                print(e)

                        #===============
                        # BROADCAST COMMAND
                        #===============

                        elif cmd.startswith("gbroadcast "):
                            sep = text.split(" ")
                            txt = text.replace(sep[0] + " ","")
                            groups = FGM.getGroupIdsJoined()
                            for group in groups:
                                try:FGM.sendMessage(group, "[ Broadcast ]\n{}".format(str(txt)))
                                except:pass
                                time.sleep(3)
                            FGM.sendMessage(to, "Berhasil broadcast ke {} group".format(str(len(groups))))

                        elif cmd.startswith("fbroadcast "):
                            sep = text.split(" ")
                            txt = text.replace(sep[0] + " ","")
                            groups = FGM.getAllContactIds()
                            for group in groups:
                                try:FGM.sendMessage(group, "[ Broadcast ]\n{}".format(str(txt)))
                                except:pass
                                time.sleep(3)
                            FGM.sendMessage(to, "Berhasil broadcast ke {} friend".format(str(len(groups))))

#============================================================================

                    elif msg.contentType == 1:
                        if settings["changePictureProfile"] == True:
                            path = FGM.downloadObjectMsg(msg_id, saveAs="tmp/{}-cpp.bin".format(time.time()))
                            settings["changePictureProfile"] = False
                            FGM.updateProfilePicture(path)
                            FGM.sendMessage(to, "Berhasil mengubah foto profile")
                            FGM.deleteFile(path)

                        if msg.toType == 2:
                            if to in settings["changeGroupPicture"]:
                                path = FGM.downloadObjectMsg(msg_id, saveAs="tmp/{}-cgp.bin".format(time.time()))
                                settings["changeGroupPicture"].remove(to)
                                FGM.updateGroupPicture(to, path)
                                FGM.sendMessage(to, "Berhasil mengubah foto group")
                                FGM.deleteFile(path)

            if op.type == 55:
                if op.param1 in read["readPoint"]:
                    if op.param2 not in read["readMember"][op.param1]:
                        read["readMember"][op.param1].append(op.param2)

    except Exception as error:
        traceback.print_tb(error.__traceback__)
        logError(error)

def run():
    while True:
        ops = FGMPoll.singleTrace(count=50)
        if ops != None:
            for op in ops:
                try:
                    FGMBot(op)
                except Exception as error:
                    logError(error)
                FGMPoll.setRevision(op.revision)

if __name__ == "__main__":
    run()
