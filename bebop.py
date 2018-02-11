import tkinter as tk
from tkinter import filedialog, simpledialog
import tkinter.font as font
import threading
import os
import pygame as pg
import sys
from settings import *

pg.init()

LIST_FONT = ("Verdana")


class MyDialog(tk.simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Number of epochs (cycles):").grid(row=0)
        self.e1 = tk.Entry(master)
        self.e1.grid(row=0, column=1)
        return self.e1  # initial focus

    def apply(self):
        first = int(self.e1.get())
        self.result = first
        # print (first)


class Bebop(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def chooseFile(self, fileNameBox):
        global fileName
        # makes list from user selection
        fileName = filedialog.askopenfilenames(initialdir="folderName", title="Select file",
                                               filetypes=(("MIDI files", "*.mid *.midi"), ("all files", "*.*")))
        getFiles = list(fileName)
        listlength = len(getFiles)

        global filePath, fileList

        filePath = []
        fileList = []

        # separate lists to split path and filename
        for i in range(0, listlength):
            (tempPath, tempList) = os.path.split((getFiles[i]))
            filePath.append(tempPath), fileList.append(tempList)

        # prints filename to make label less messy
        for i in range(0, listlength):
            fileNameBox.insert(tk.END, str(i) + ". " + fileList[i] + '\n')

        for i in range(0, len(fileList)):
            print(str(i) + ". " + fileList[i] + '\n')

    def playSong(self, thesong):
        thesongpath = (sys.path[0] + '\RNN\music_outputs' + "\\" + thesong[3:])
        print(thesongpath)
        pg.mixer.music.load(thesongpath)
        pg.mixer.music.play()

    def stopSong(self):
        pg.mixer.music.stop()

    def quit(self):
        exit()

    def updateJukeList(self, jukelistbox):
        jukelistbox.delete(0, tk.END)
        songfiles_path = (sys.path[0] + '\RNN\music_outputs')
        songfiles = [f for f in os.listdir(songfiles_path)]
        for i in range(0, len(songfiles)):
            jukelistbox.insert(tk.END, str(i + 1) + ". " + songfiles[i])

    def createSongList(self):
        songList = []
        for i in range(0, len(filePath)):
            songList.append(filePath[i] + '/' + fileList[i])
        return songList

    def makeSong(self):
        ui_num_epochs = MyDialog(self)
        num_epochs = ui_num_epochs.result
        print("# of epochs: ", num_epochs)

        if (num_epochs == None):
            # no epochs set; default: 50
            print("No epochs set, defaulting to 50 epochs")
            num_epochs = 50

        songList = self.createSongList()
        songList = ','.join(songList)
        # weight initialize [weight_initialize]
        weightfile = (sys.path[0] + '\RNN\weight_initializations.py')
        os.system('py {} {}'.format(weightfile, str(songList)))

        # print(num_epochs)
        # rnn/rbm train model [rnn_rbm_train (num_epochs)]
        trainfile = (sys.path[0] + '\RNN\\rnn_rbm_train.py')
        os.system('py {} {} {}'.format(trainfile, num_epochs, songList))

        # generate [rnn_rbm_generate (path_to_ckpt)]
        # RNN.rnn_rbm_generate('parameter_checkpoints/epoch_49.ckpt')
        generatefile = (sys.path[0] + '\RNN\\rnn_rbm_generate.py')
        epochpath = (sys.path[0] + '\RNN\parameter_checkpoints\epoch_{}.ckpt'.format(num_epochs - 1))
        os.system('py {} {} {}'.format(generatefile, epochpath, songList))

        # change pages
        self.show_frame(PageTwo)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        fullboxWidth = 900
        fullboxHeight = 700
        buttonHeight = 450
        buttonWidth = 350

        Rockwell = font.Font(family='Helvetica', size=46)

        mainFrame = tk.Frame(self, bg=blueblack, width=fullboxWidth, height=fullboxHeight)
        mainFrame.grid(row=0, column=0, columnspan=5, rowspan=3)

        label = tk.Label(self, text="Bineural Beats", width=20, height=1, bg=blueblack, fg=white)
        label.config(font=("Rockwell", 44))
        label.grid(row=0, column=1, columnspan=3)

        musicLabel = tk.Label(self, text="Music Maker", width=17, height=1, bg=blueblack, fg=white)
        musicLabel.config(font=("Rockwell", 30))
        musicLabel.grid(row=1, column=1, columnspan=1, sticky="S")

        global musicmakerButton
        musicmakerButton = tk.PhotoImage(file="musicmakermain.png")
        button = tk.Button(self, image=musicmakerButton, font=Rockwell, height=buttonHeight, width=buttonWidth,
                           command=lambda: controller.show_frame(PageOne), fg=blueblack)
        button.grid(row=2, column=1, columnspan=1)

        jukeLabel = tk.Label(self, text="Boombox", width=10, height=1, bg=blueblack, fg=white)
        jukeLabel.config(font=("Rockwell", 30))
        jukeLabel.grid(row=1, column=2, sticky="S")

        global jukeboxButton
        jukeboxButton = tk.PhotoImage(file="jukeboxmain.png")
        button2 = tk.Button(self, image=jukeboxButton, font=Rockwell, height=buttonHeight, width=buttonWidth,
                            command=lambda: controller.show_frame(PageTwo))
        button2.grid(row=2, column=2, columnspan=1)


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        topBarWidth = 900;
        topBarHeight = 150;
        botBarWidth = 900;
        botBarHeight = 550;

        buttonWidth = 175
        buttonHeight = 80

        Rockwell = font.Font(family='Rockwell', size=14)

        topBar = tk.Frame(self, bg=blueblack, width=topBarWidth, height=topBarHeight)
        topBar.grid(row=0, columnspan=5)

        botBar = tk.Frame(self, bg=blueblack, width=botBarWidth, height=botBarHeight)
        botBar.grid(row=1, columnspan=5, rowspan=4)

        titleLabel = tk.Label(self, text="Music Maker", bg=blueblack, fg=white, font=(Rockwell, 10))
        titleLabel.config(font=("Rockwell", 44))
        titleLabel.grid(row=0, column=1, columnspan=3)

        global homeImgMaker
        homeImgMaker = tk.PhotoImage(file="backbutton.png")
        homebutton = tk.Button(self, height=50, borderwidth=1, width=100, image=homeImgMaker,
                               command=lambda: controller.show_frame(StartPage))
        homebutton.grid(row=0, column=0)

        global quitImgMaker
        quitImgMaker = tk.PhotoImage(file="exitbutton.png")
        quitButton = tk.Button(self, borderwidth=1, height=50, width=100, image=quitImgMaker, command=quit)
        quitButton.grid(row=0, column=4)

        global bgMaker
        bgMaker = tk.PhotoImage(file="musicmaker700.png")
        background = tk.Label(self, image=bgMaker, width=botBarWidth - 5, height=botBarHeight - 5, bg=cobalt, fg=white)
        background.grid(row=1, columnspan=5, rowspan=4)

        fileNameBox = tk.Listbox(self, width=50, height=20, fg=white, bg=blueblack, font=(LIST_FONT, 10),
                                 selectmode=tk.EXTENDED)
        fileNameBox.grid(row=1, column=1, rowspan=3)

        global addImg
        addImg = tk.PhotoImage(file="addbutton.png")
        openButton = tk.Button(self, height=buttonHeight, width=buttonWidth, image=addImg, font=Rockwell,
                               command=lambda: controller.chooseFile(fileNameBox))
        openButton.grid(row=1, column=3)

        global deleteImg
        deleteImg = tk.PhotoImage(file="removebutton.png")
        # bug: doesn't delete entire selection, only last item selected
        directoryButton = tk.Button(self, height=buttonHeight, width=buttonWidth, image=deleteImg, font=Rockwell,
                                    command=lambda fileNameBox=fileNameBox: fileNameBox.delete(tk.ACTIVE))
        directoryButton.grid(row=2, column=3)

        # todo: make the dialogue box move to center
        global createImg
        createImg = tk.PhotoImage(file="makebutton.png")
        playButton = tk.Button(self, height=buttonHeight, width=buttonWidth, image=createImg, font=Rockwell,
                               command=controller.makeSong)
        playButton.grid(row=3, column=3)


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        topBarWidth = 900;
        topBarHeight = 150;
        botBarWidth = 900;
        botBarHeight = 550;

        buttonWidth = 175
        buttonHeight = 80

        Rockwell = font.Font(family='Rockwell', size=14)

        topBar = tk.Frame(self, bg=blueblack, width=topBarWidth, height=topBarHeight)
        topBar.grid(row=0, columnspan=5)

        botBar = tk.Frame(self, bg=blueblack, width=botBarWidth, height=botBarHeight)
        botBar.grid(row=1, columnspan=5, rowspan=4)

        global bgJuke
        bgJuke = tk.PhotoImage(file="jukebox700.png")
        background = tk.Label(self, image=bgJuke, width=botBarWidth - 5, height=botBarHeight - 5, bg=cobalt, fg=white)
        background.grid(row=1, columnspan=5, rowspan=4)

        titleLabel = tk.Label(self, text="Boombox", bg=blueblack, fg=white)
        titleLabel.config(font=("Rockwell", 44))
        titleLabel.grid(row=0, column=1, columnspan=3)

        global homeImgJuke
        homeImgJuke = tk.PhotoImage(file="backbutton.png")
        homebutton = tk.Button(self, height=50, borderwidth=1, width=100, image=homeImgJuke,
                               command=lambda: controller.show_frame(StartPage))
        homebutton.grid(row=0, column=0)

        global quitJuke
        quitJuke = tk.PhotoImage(file="exitbutton.png")
        quitButton = tk.Button(self, borderwidth=1, height=50, width=100, image=quitJuke, command=quit)
        quitButton.grid(row=0, column=4)

        global refreshImg
        refreshImg = tk.PhotoImage(file="refreshbutton.png")
        pauseButton = tk.Button(self, height=46, width=46, image=refreshImg, font=Rockwell,
                                command=lambda: controller.updateJukeList(songFileNameBox))
        pauseButton.grid(row=1, column=0)

        songFileNameBox = tk.Listbox(self, width=50, height=20, fg=white, bg=blueblack, font=(LIST_FONT, 10),
                                     selectmode=tk.SINGLE)
        songFileNameBox.grid(row=1, column=1, rowspan=3)

        # setup listbox
        songfiles_path = (sys.path[0] + '\RNN\music_outputs')
        songfiles = [f for f in os.listdir(songfiles_path)]
        print(songfiles)
        for i in range(0, len(songfiles)):
            songFileNameBox.insert(tk.END, str(i + 1) + ". " + songfiles[i])

        global playImg
        playImg = tk.PhotoImage(file="playbutton.png")
        openButton = tk.Button(self, height=buttonHeight, width=buttonWidth, image=playImg, font=Rockwell,
                               command=lambda: controller.playSong(songFileNameBox.get(songFileNameBox.curselection())))
        openButton.grid(row=1, column=3)

        global stopImg
        stopImg = tk.PhotoImage(file="stopbutton.png")
        quitSongButton = tk.Button(self, height=buttonHeight, width=buttonWidth, image=stopImg, font=Rockwell,
                                   command=lambda: controller.stopSong())
        quitSongButton.grid(row=2, column=3)


app = Bebop()
app.title("Bineural Beats")
app.mainloop()
