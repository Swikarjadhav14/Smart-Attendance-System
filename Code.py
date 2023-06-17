import webbrowser
from tkinter import *
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime

def add_photo(frame, image_path, desired_size, position):
    image = Image.open(image_path)
    image = image.resize(desired_size, Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    label = Label(frame, image=photo)
    label.image = photo  # Store a reference to the image to prevent garbage collection
    label.place(x=position[0], y=position[1])

def next():
    signin_frame1 = tk.Frame(root, bg="white", bd=6, relief="solid" ,highlightthickness=9, highlightbackground="pink")
    signin_frame1.place(relx=0.5, rely=0.62, relwidth=0.4, relheight=0.7, anchor="w")
    button1 = tk.Button(signin_frame1, text="Face Detection", font=("Helvetica", 20, "bold"), bg="white", fg="black", relief="solid", bd=2,padx=5,command=face_recog)
    button1.place(relx=0.08, rely=0.35)
    button1.bind("<Enter>", on_enter)
    button1.bind("<Leave>", on_leave)
    submit_button.bind("<Enter>", on_enter)
    submit_button.bind("<Leave>", on_leave)
    button2 = tk.Button(signin_frame1, text="Fingerprint", font=("Helvetica", 20, "bold"), bg="white", fg="black", relief="solid", bd=2,padx=28)
    button2.place(relx=0.52, rely=0.35)
    button2.bind("<Enter>", on_enter)
    button2.bind("<Leave>", on_leave)
    tommy_button = tk.Label(signin_frame1, text="Click on any one mode of attendance",font=("Helvetica", 20, "bold"), bg="white", fg="black", padx=20, pady=10, relief="solid", bd=2, highlightthickness=1, highlightbackground="pink" )
    tommy_button.place(relx=0.04, rely=0.13)
    add_photo(signin_frame1, "next1.jpg", (231, 270), (45, 280))
    add_photo(signin_frame1, "next2.jpg", (230, 270), (300, 280))


def on_enter(event):
    event.widget.config(bg='red', fg='white')

def on_leave(event):
    event.widget.config(bg='white', fg='black')

root = tk.Tk()
root.attributes('-fullscreen', True)
root.title("SMART ATTENDANCE SYSTEM")

swikar_image = face_recognition.load_image_file("faces/swikar.jpg")
swikar_encoding = face_recognition.face_encodings(swikar_image)[0]

shounak_image = face_recognition.load_image_file("faces/shounak.jpg")
shounak_encoding = face_recognition.face_encodings(shounak_image)[0]

hitesh_image = face_recognition.load_image_file("faces/hitesh.jpg")
hitesh_encoding = face_recognition.face_encodings(hitesh_image)[0]

yash_image = face_recognition.load_image_file("faces/yash.jpg")
yash_encoding = face_recognition.face_encodings(yash_image)[0]

def face_recog():
    video_capture = cv2.VideoCapture(0)
    known_face_encodings = [swikar_encoding, shounak_encoding, hitesh_encoding, yash_encoding]
    known_face_names = ["Swikar Jadhav", "Shounak Mulay", "Hitesh Pawar", "Yash Adhikari"]
    students = known_face_names.copy()

    face_locations = []
    face_encodings = []

    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")

    f = open(f"{current_date}.csv", "w+", newline="")
    lnwriter = csv.writer(f)

    while True:
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distance)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                name_with_box = f"({name})"  #({round(1 - face_distance[best_match_index]})

            # Scale back up face locations
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

            # Draw a rectangle around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw name above the face
                font = cv2.FONT_HERSHEY_DUPLEX
                font_scale = 0.75
                text_width, text_height = cv2.getTextSize(name_with_box, font, font_scale, 1)[0]
                cv2.rectangle(frame, (left, top - text_height - 10), (left + text_width + 10, top), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name_with_box, (left + 5, top - 7), font, font_scale, (255, 255, 255), 1)

                if name in students:
                    students.remove(name)
                    current_time = now.strftime("%H:%M:%S")
                    lnwriter.writerow([name, current_time])

        cv2.imshow("Face Recognition Attendance System", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def open_link(event):
    webbrowser.open("https://pict.edu") 

# image = Image.open("space1.jpg")  # Replace "background.jpg" with the path to your image file
# image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))  # Resize the image to fit the screen
# background_image = ImageTk.PhotoImage(image)

background_label = tk.Label(root, bg='#29281f')
background_label.place(x=0, y=0, relwidth=1, relheight=1)  
title_label = tk.Label(root, text="Face Recognition Attendance System", font=("Helvetica", 32, "bold"), bg="white", fg="black", padx=30, pady=30, relief="solid", bd=5, highlightthickness=5, highlightbackground="#F2BED1")
title_label.place(relx=0.5, rely=0.1, anchor="center")  
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
datetime_label = tk.Label(root, text=current_datetime, font=("Helvetica",21), bg="white", fg="black")
datetime_label.place(relx=0.5, rely=0.215, anchor="center")  # Position the label below the title
signin_frame = tk.Frame(root, bg="#FCE9F1", bd=6, relief="solid" ,highlightthickness=9, highlightbackground="white")
signin_frame.place(relx=0.5, rely=0.62, relwidth=0.4, relheight=0.7, anchor="w") 

signin_heading = tk.Label(signin_frame, text="Administrator Login", font=("Helvetica", 30, "italic"), bg="white", fg="black", bd=2, relief="solid",highlightthickness=4, highlightbackground="grey")
signin_heading.place(relx=0.17, rely=0.05)
username_label = tk.Label(signin_frame, text="USERNAME", font=("Helvetica", 22,"bold"), fg="black",bg="#FCE9F1",relief="solid",highlightthickness=0, highlightbackground="red")
username_label.place(relx=0.09, rely=0.42+0.06)
username_entry = tk.Entry(signin_frame, font=("Helvetica",22 ), fg="black", relief="solid", bd=2,bg="white")
username_entry.place(relx=0.4, rely=0.42+0.06)
password_label = tk.Label(signin_frame, text="PASSWORD", font=("Helvetica", 22,"bold"),bg="#FCE9F1",  fg="black",relief="solid",highlightthickness=0, highlightbackground="red")
password_label.place(relx=0.09, rely=0.56+0.06)
password_entry = tk.Entry(signin_frame, show="*", font=("Helvetica", 22), fg="black", relief="solid", bd=2,bg="white")
password_entry.place(relx=0.4, rely=0.56+0.06)
submit_button = tk.Button(signin_frame, text="Submit", font=("Helvetica", 22, "bold"),  fg="black", relief="solid", bd=2,highlightthickness=3, highlightbackground="red",command=next)
submit_button.place(relx=0.4,rely=0.76)
submit_button.bind("<Enter>", on_enter)
submit_button.bind("<Leave>", on_leave)
link_label = ttk.Label(signin_frame, text="PICT PUNE", cursor="hand2", foreground="blue",font=("Helvetica", 20, "bold"),)
link_label.pack(side='bottom')
link_label.bind("<Button-1>", open_link)

picture_frame = tk.Frame(root,bg="azure2", bd=6, relief="solid" ,highlightthickness=9, highlightbackground="white")
picture_frame.place(relx=0.28, rely=0.62, relwidth=0.44, relheight=0.7, anchor="center") 
add_photo(picture_frame, "How-Does-the-Attendance-Management-System-Help-the-Employees.jpg", (642, 570), (0, 0))
add_photo(signin_frame, "college.jpg", (250,150), (150,100))

root.mainloop()
