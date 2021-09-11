import words_reader
import random
from tkinter import *
from tkinter import scrolledtext, StringVar, messagebox

BACKGROUNDCOLOR = "#BFD8B8"
font=("Helvetica", 8)
font_text=("Helvetica", 14)

LABELCOLOR = "#E7EAB5"
BUTTONCOLOR = "#F1F7E7"

reader = words_reader.WordReader()
words_list = reader.read_words()

window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUNDCOLOR)
var = StringVar()
word_count = 0
row_count = 1
last_index = 0
scroll_text_index = 0
right_words = 0
countdown_time = 60
start = False
total_characters = 1
restart_on =True


def restart():
    global restart_on
    global word_count
    global row_count
    global last_index
    global right_words
    global total_characters
    global words_list
    global scroll_text_index
    global countdown_time
    global start
    text_window.delete(index1="1.0",index2=END)
    get_words()
    restart_on=True
    word_count = 0
    row_count = 1
    last_index = 0
    scroll_text_index = 0
    right_words = 0
    countdown_time = 60
    start = False
    total_characters = 1
    correct_cpm_label_counter.config(text=f"{0}")
    wpm_label_counter.config(text=f"{0}")
    try:
        text_entry.config(state="enabled")
    except:
        pass


def get_words():
    global words_list
    reader = words_reader.WordReader()
    words_list = reader.read_words()
    k=1
    for i in range(0, len(words_list)):
        if k%4==0:
            text_window.insert(INSERT, random.choice(words_list) + "\n")
        else:

            text_window.insert(INSERT, random.choice(words_list) + " ")
        k+=1


def callback(my_var, indx, mode):
    global restart_on
    text_in_entry = var.get()
    if " " in var.get():
        restart_on = False
        check_words(text_in_entry)
        text_entry.delete(first=0, last=len(text_in_entry)+1)

def count_down():
    global start
    global countdown_time
    if not restart_on:
        start=True
        countdown_time -= 1
        time_left_label_counter.config(text=f"{countdown_time}s")
        cpm = round((total_characters*60)/(60-countdown_time),1)
        correct_cpm_label_counter.config(text=f"{cpm}")
        wpm = round((right_words*60)/(60-countdown_time),1)
        wpm_label_counter.config(text=f"{wpm}")

        if countdown_time <1:
            start = False
            text_entry.config(state="disabled")
            messagebox.showinfo(title="Results", message=f"Congrats you wrote at {wpm} words per minute speed !")
        if start==True:
            window.after(1000, count_down)
    else:
        time_left_label_counter.config(text=f"{countdown_time}s")
        correct_cpm_label_counter.config(text=f"{0}")
        wpm_label_counter.config(text=f"{0}")

def check_words(word):
    global word_count
    global row_count
    global last_index
    global right_words
    global total_characters
    words_row = text_window.get(f"{row_count}.0", f"{row_count+1}.0").split()
    if not start and not restart_on:
        count_down()
    if words_row[word_count] == word.replace(" ", ""):
        right_words += 1
        text_window.delete(f"{row_count}.{last_index}", f"{row_count}.{len(words_row[word_count])+last_index}")
        text_window.insert(f"{row_count}.{last_index}", words_row[word_count], ("text"))
        word_count += 1
        last_index = last_index+len(word)
        total_characters += len(word)
        text_window.tag_config("text", background="green")

    else:
        text_window.delete(f"{row_count}.{last_index}", f"{row_count}.{len(words_row[word_count]) + last_index}")
        text_window.insert(f"{row_count}.{last_index}", words_row[word_count], ("wrong"))
        last_index = last_index + len(words_row[word_count])+1
        word_count += 1
        text_window.tag_config("wrong", background="red")


    if word_count == 4:
        word_count = 0
        row_count += 1
        last_index = 0
    if row_count%2 ==0:
        text_window.see(index=f"{row_count+2}.0")



main_canvas = Canvas(height=300, width=300, bg=BACKGROUNDCOLOR, highlightthickness=0)
main_canvas.grid(column=0, row=0)
logo_image = PhotoImage(file="./image/logo.png")
logo = main_canvas.create_image(200, 200, image=logo_image)

first_frame = Frame(window)
first_frame.grid(row=1, column=0)

correct_cpm_label = Label(first_frame, text="Corrected CPM: ", width=15, bg=BACKGROUNDCOLOR, font=font)
correct_cpm_label.grid(column=2, row=0)

correct_cpm_label_counter = Label(first_frame, text=" ", width=10, bg=LABELCOLOR, font=font)
correct_cpm_label_counter.grid(column=3, row=0)


wpm_label = Label(first_frame, text="Words / minute: ", width=15, bg=BACKGROUNDCOLOR, font=font)
wpm_label.grid(column=4, row=0)


wpm_label_counter = Label(first_frame, text=" ", width=10, bg=LABELCOLOR, font=font)
wpm_label_counter.grid(column=5, row=0)


time_left_label = Label(first_frame, text="Time left: ", width=10, bg=BACKGROUNDCOLOR, font=font)
time_left_label.grid(column=6, row=0)



time_left_label_counter = Label(first_frame, text=f"{countdown_time} s", width=10, bg=LABELCOLOR, font=font)
time_left_label_counter.grid(column=7, row=0)

secound_frame = Frame(window, bg=BACKGROUNDCOLOR)
secound_frame.grid(row=2, column=0,ipadx=20, padx=20, ipady=5, pady=10)
restart_button = Button(secound_frame, text="Restart",activebackground=BUTTONCOLOR,
                        bg=LABELCOLOR,relief="groove", width=15, padx=20, font=font, command=restart)
restart_button.grid(row=0, column=0, sticky="w")


text_window = scrolledtext.ScrolledText(width=35, height=7, font=font_text, bg=LABELCOLOR)
text_window.grid(column=0, row=3)

var.trace_add("write",callback=callback)

text_entry = Entry(width=30, font=font_text, bg=LABELCOLOR,textvariable=var)
text_entry.grid(column=0, row=4, pady=20)

if start == False:
    get_words()







window.mainloop()