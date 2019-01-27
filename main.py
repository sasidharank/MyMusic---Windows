import os.path
import webbrowser
import time
import threading
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from pygame import *
from mutagen.mp3 import MP3
from tkinter import ttk
from ttkthemes import themed_tk as tk

root = tk.ThemedTk()
root.get_themes()
root.set_theme('keramik')

# To auto fix the root window in center of the screen
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth() / 2.5 - windowWidth / 2)
positionDown = int(root.winfo_screenheight() / 3 - windowHeight / 2)
root.geometry("+{}+{}".format(positionRight, positionDown))

mixer.init()  # initializing the mixer
root.title('MyMusic')
root.iconbitmap('images/micon.ico')
# menu bar creation
menu_bar = Menu(root)
root.config(menu=menu_bar)
# sub menu creation
sub_menu = Menu(menu_bar, tearoff=0)
status_bar = Label(root, text='Welcome to MyMusic', relief=SUNKEN, anchor=W, font='Arial 10 bold', fg='#f46842')
status_bar.pack(side=BOTTOM, fill=X)


def about_us():
    tkinter.messagebox.showinfo('About MyMusic', 'This is a Python GUI Music player by Sasidharan K')


def contact():
    webbrowser.open_new("https://sasiworks.herokuapp.com/contact")


def update_progress(l):
    global paused
    pos = 1
    while pos <= l and mixer.music.get_busy():
        if paused:
            continue
        else:
            pos_percent = pos / l * 100
            progress_bar["value"] = pos_percent
            time.delay(1000)
            pos += 1


def browse_file():
    global song_file_path
    song_file_path = filedialog.askopenfilenames(title='Choose a Audio File')
    for song in song_file_path:
        add_song(song)


def add_song(sf):
    filename = os.path.basename(sf)
    index = 0
    listbox.insert(index, filename)
    playlist.insert(index, sf)
    index += 1


def delete_song():
    try:
        selected_song = listbox.curselection()
        selected_song = int(selected_song[0])
        listbox.delete(selected_song)
        playlist.pop(selected_song)
    except IndexError or NameError:
        status_bar['text'] = 'No Music Selected'


def show_details(play_it):
    file_format = os.path.splitext(play_it)
    if file_format[1] == '.mp3':
        audio = MP3(play_it)
        length = audio.info.length
    else:
        a = mixer.Sound(play_it)
        length = a.get_length()

    mins, secs = divmod(length, 60)
    time_format = '{:02d}:{:02d}'.format(round(mins), round(secs))
    lengthlabel['text'] = 'Music Length ' + '- ' + time_format
    thread1 = threading.Thread(target=remaining_count, args=(round(length),))
    thread1.start()
    thread2 = threading.Thread(target=update_progress, args=(round(length),))
    thread2.start()


def remaining_count(l):
    global paused
    length = 1
    while length <= l and mixer.music.get_busy():  # mixer.music.get_busy() - If stop pressed it return false
        if paused:  # If paused is True ,continue ignore all below codes ,wait for unpause
            continue
        else:  # If not paused execute below code
            mins, secs = divmod(length, 60)
            time_format = '{:02d}:{:02d}'.format(round(mins), round(secs))
            currenttimelabel['text'] = 'Playing Time ' + '- ' + time_format
            time.delay(1000)
            length += 1


def play_music():
    global paused
    global stopped
    if stopped:
        try:
            selected_song = listbox.curselection()
            selected_song = int(selected_song[0])
            global play_it
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            status_bar['text'] = 'Playing Music' + ' - ' + os.path.basename(play_it)
            stopped = FALSE
        except NameError and IndexError:
            status_bar['text'] = 'Music Not Found'
    if paused:
        try:
            mixer.music.unpause()
            status_bar['text'] = 'Music Resumed' + ' - ' + os.path.basename(play_it)
            paused = FALSE
        except IndexError or NameError:
            status_bar['text'] = 'Music Not Found'

    else:
        try:
            stop_music()
            time.delay(1000)
            selected_song = listbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            status_bar['text'] = 'Playing Music' + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except IndexError or NameError:
            tkinter.messagebox.showerror('Music Not Found', 'Add (+) and "Select" your Music to Play')
            status_bar['text'] = 'Music Not Found'


def stop_music():
    global stopped
    stopped = True
    mixer.music.stop()
    status_bar['text'] = 'Music Stopped'


def pause_music():
    global paused
    global stopped
    paused = TRUE
    stopped = FALSE
    mixer.music.pause()
    status_bar['text'] = 'Music Paused'


def rewind_music():
    try:
        global paused
        global stopped
        paused = FALSE
        stopped = TRUE
        play_music()
    except IndexError:
        status_bar['text'] = 'Add Your Music'


def mute_unmute():
    global sound
    if sound:
        mixer.music.set_volume(0)
        sound_btn.configure(image=mute_pic)
        scale_wid.set(0)
        status_bar['text'] = 'Sound OFF'
        sound = FALSE
    else:
        try:
            mixer.music.set_volume(50)
            sound_btn.configure(image=unmute_pic)
            scale_wid.set(50)
            status_bar['text'] = 'Sound ON'
            sound = TRUE
        except NameError:
            status_bar['text'] = 'Playing Music' + ' - ' + os.path.basename(play_it)


def vol_control(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


def on_close():
    if tkinter.messagebox.askokcancel('Warning', 'Are you sure want to exit ?'):
        stop_music()
        root.destroy()


# ROOT contains - Status bar which is along the bottom of window,Leftframe,Rightframe
# Leftframe - list box and 2 buttons
# Rightframe - top,middle,bottom child frames od parent Rightframe
# topframe-labels
# middleframe-play,pause,stop
# bottomframe-scale,rewind button,mute button

# Initial values of playlist, paused, stopped, sound
playlist = []
paused = False
stopped = False
sound = TRUE

menu_bar.add_cascade(label="File", menu=sub_menu)  # sub menu / cascade
sub_menu.add_command(label="Upload", command=browse_file)
sub_menu.add_command(label="Exit", command=root.destroy)

sub_menu = Menu(menu_bar, tearoff=0)  # sub other menu creation
menu_bar.add_cascade(label="Help", menu=sub_menu)
sub_menu.add_command(label="About", command=about_us)
sub_menu.add_command(label="Contact", command=contact)

left_frame = Frame(root)
left_frame.pack(side=LEFT, padx=30, pady=30)

right_frame = Frame(root)
right_frame.pack(pady=20, padx=10)

top_frame = Frame(right_frame)
top_frame.pack()

lengthlabel = Label(top_frame, text='Music Length : --:--', relief=GROOVE, bg='#ffff80')
lengthlabel.pack()

currenttimelabel = Label(top_frame, text='Playing Time : --:--', relief=FLAT, fg='green')
currenttimelabel.pack(pady=10)

progress_bar = ttk.Progressbar(top_frame, mode='determinate', length=200, value=0)
progress_bar.pack()

listbox = Listbox(left_frame, bg='#ff8566')
listbox.pack()

left_frame_add = ttk.Button(left_frame, text='+ ADD', command=browse_file)
left_frame_add.pack(side=LEFT, pady=(15, 0), padx=10)

left_frame_del = ttk.Button(left_frame, text=' -  DEL', command=delete_song)
left_frame_del.pack(side=LEFT, pady=(15, 0))

middle_frame = Frame(right_frame)
middle_frame.pack(padx=10, pady=(20, 20))

bottom_frame = Frame(right_frame)
bottom_frame.pack(padx=10, pady=(13, 0))

play_pic = PhotoImage(file='images/play.png')
play_btn = ttk.Button(middle_frame, image=play_pic, command=play_music)
play_btn.grid(column=0, row=0, padx=10)

stop_pic = PhotoImage(file='images/stop.png')
stop_btn = ttk.Button(middle_frame, image=stop_pic, command=stop_music)
stop_btn.grid(column=2, row=0, padx=10)

pause_pic = PhotoImage(file='images/pause.png')
pause_btn = ttk.Button(middle_frame, image=pause_pic, command=pause_music)
pause_btn.grid(column=1, row=0, padx=10)

rewind_pic = PhotoImage(file='images/replay.png')
rewind_btn = ttk.Button(bottom_frame, image=rewind_pic, command=rewind_music)
rewind_btn.grid(row=0, column=0, padx=5)

mute_pic = PhotoImage(file='images/mute.png')
unmute_pic = PhotoImage(file='images/unmute.png')
sound_btn = ttk.Button(bottom_frame, image=unmute_pic, command=mute_unmute)
sound_btn.grid(row=0, column=1, padx=5)

scale_wid = ttk.Scale(bottom_frame, from_=0, to=100, orient=HORIZONTAL, command=vol_control)
scale_wid.set(50)
mixer.music.set_volume(50)
scale_wid.grid(row=0, column=2, padx=5)

root.protocol('WM_DELETE_WINDOW', on_close)
root.resizable(0, 0)
root.mainloop()
