import os
import tkinter as tk
from tkinter import messagebox

import bcrypt
import cv2
import face_recognition
import mysql.connector
import numpy as np
from PIL import Image, ImageTk

# Create the main application window
root = tk.Tk()
root.title("NebulaSource")
root.configure(background="black")


def connect_to_mysql():
    """Connect using configuration supplied through environment variables."""
    required_settings = {
        "host": os.getenv("NEBULA_DB_HOST"),
        "user": os.getenv("NEBULA_DB_USER"),
        "password": os.getenv("NEBULA_DB_PASSWORD"),
        "database": os.getenv("NEBULA_DB_NAME"),
    }
    missing_settings = [
        variable
        for variable, value in {
            "NEBULA_DB_HOST": required_settings["host"],
            "NEBULA_DB_USER": required_settings["user"],
            "NEBULA_DB_PASSWORD": required_settings["password"],
            "NEBULA_DB_NAME": required_settings["database"],
        }.items()
        if not value
    ]
    if missing_settings:
        messagebox.showerror(
            "Configuration error",
            "Missing database configuration: " + ", ".join(missing_settings),
        )
        return None

    try:
        conn = mysql.connector.connect(**required_settings)
        if conn.is_connected():
            print("Connected to MySQL database")
            return conn
    except mysql.connector.Error as err:
        print("Error:", err)
        return None


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def serialize_face_encoding(face_encoding):
    return ",".join(map(str, face_encoding.tolist()))


def deserialize_face_encoding(encoded_face):
    return np.array(list(map(float, encoded_face.split(","))))


def register_user():
    username = username_entry.get()
    password = os.getenv("NEBULA_DEFAULT_PASSWORD")
    if not password:
        messagebox.showerror(
            "Configuration error",
            "Set NEBULA_DEFAULT_PASSWORD before registering a user.",
        )
        return

    # Capture and serialize the user's face encoding.
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        messagebox.showerror("Camera error", "Unable to access the camera.")
        return

    serialized_face_encoding = None
    try:
        while True:
            ret, frame = video_capture.read()
            if not ret:
                messagebox.showerror("Camera error", "Unable to read from the camera.")
                break

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_frame = small_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_frame)
            if face_locations:
                face_encoding = face_recognition.face_encodings(
                    rgb_frame, face_locations
                )[0]
                serialized_face_encoding = serialize_face_encoding(face_encoding)
                break

            cv2.imshow("Capture Face", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        video_capture.release()
        cv2.destroyAllWindows()

    if serialized_face_encoding is None:
        messagebox.showinfo(
            "Registration cancelled",
            "No face was captured; the user was not registered.",
        )
        return

    hashed_password = hash_password(password)

    conn = connect_to_mysql()
    if conn is None:
        return

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            messagebox.showerror("Registration", "Username already exists")
            return

        cursor.execute(
            "INSERT INTO users (username, password, face_encoding) VALUES (%s, %s, %s)",
            (username, hashed_password, serialized_face_encoding),
        )
        conn.commit()
        messagebox.showinfo("Registration", "User registered successfully")

    except mysql.connector.Error as err:
        print("Error:", err)
        messagebox.showerror("Registration", "An error occurred during registration")

    finally:
        cursor.close()
        conn.close()


# ... Rest of your code ...

# Start the main event loop
root.mainloop()
