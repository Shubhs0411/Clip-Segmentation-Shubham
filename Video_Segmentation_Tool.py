#!/usr/bin/env python
# coding: utf-8

# In[2]:
"""
    A Project by Shubham Laxmikant Deshmukh.
"""

"""
    Importing libraries for the project.
"""

import os
import cv2 
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk  
import moviepy.editor as mp
from tkinter import Label
import os

def shot_boundary_detection(video_path, threshold=100):
    """
        Detect shot boundaries in a video based on histogram differences between frames.

        Args:
        - video_path (str): Path to the input video file.
        - threshold (int): Threshold for detecting shot boundaries.

        Returns:
        - shot_boundaries (list): List of timestamps representing shot boundaries.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Couldn't open video file")
        return
    
    # Initialize variables
    prev_frame_hist = None
    shot_boundaries = [0]
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate histogram
        hist = cv2.calcHist([gray_frame], [0], None, [256], [0, 256])
        
        # Normalize histogram
        cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        
        # Check if it's the first frame
        if prev_frame_hist is None:
            prev_frame_hist = hist
            continue
        
        # Calculate histogram difference
        hist_diff = cv2.compareHist(prev_frame_hist, hist, cv2.HISTCMP_BHATTACHARYYA)
        
        # If the difference is above the threshold, it indicates a shot boundary
        if hist_diff > threshold:
            shot_boundaries.append(cap.get(cv2.CAP_PROP_POS_MSEC))
        
        # Update previous frame histogram
        prev_frame_hist = hist
    
    cap.release()
    
    return shot_boundaries

def clip_video(video_path, shot_boundaries, output_dir):
    """
        Clip the input video based on detected shot boundaries and save each segment as a separate file.

        Args:
        - video_path (str): Path to the input video file.
        - shot_boundaries (list): List of timestamps representing shot boundaries.
        - output_dir (str): Directory to save the clipped video segments.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Couldn't open video file")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Iterate over shot boundaries and create clips
    for i, boundary in enumerate(shot_boundaries):
        start_time = boundary / 1000  # convert milliseconds to seconds
        end_time = (shot_boundaries[i + 1] / 1000)-0.1 if i < len(shot_boundaries) - 1 else None
        
        # Set capture to start at the beginning of the clip
        cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)
        
        # Initialize VideoWriter for the clip
        clip_name = os.path.join(output_dir, f"clip_{i}.mp4")
        out = cv2.VideoWriter(clip_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
        
        # Read frames and write to the clip until the end time
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Write frame to the clip
            out.write(frame)
            
            # Check if reached the end time of the clip
            if end_time and cap.get(cv2.CAP_PROP_POS_MSEC) >= end_time * 1000:
                break
        
        # Release VideoWriter and move to the next clip
        out.release()

    cap.release()

def clip_audio(video_path, shot_boundaries, output_dir):
    """
        Clip the audio of the input video based on detected shot boundaries and save each segment as a separate file.

        Args:
        - video_path (str): Path to the input video file.
        - shot_boundaries (list): List of timestamps representing shot boundaries.
        - output_dir (str): Directory to save the clipped audio segments.
    """
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    
    # Iterate over shot boundaries and create audio clips
    for i, boundary in enumerate(shot_boundaries):
        start_time = boundary / 1000  # convert milliseconds to seconds
        end_time = (shot_boundaries[i + 1] / 1000)-0.1 if i < len(shot_boundaries) - 1 else None
        
        # Clip the audio
        audio_clip = audio.subclip(start_time, end_time)
        
        # Write audio clip to file
        audio_clip.write_audiofile(os.path.join(output_dir, f"audio_clip_{i}.mp3"))

def combine_video_audio(video_dir, audio_dir, output_dir):
    """
        Combine the clipped video and audio segments into final clips.

        Args:
        - video_dir (str): Directory containing the clipped video segments.
        - audio_dir (str): Directory containing the clipped audio segments.
        - output_dir (str): Directory to save the combined video clips.
    """
    video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.mp3')]
    
    # Ensure equal number of video and audio clips
    num_clips = min(len(video_files), len(audio_files))
    
    for i in range(num_clips):
        video_path = os.path.join(video_dir, f"clip_{i}.mp4")
        audio_path = os.path.join(audio_dir, f"audio_clip_{i}.mp3")
        
        # Load video clip
        video_clip = mp.VideoFileClip(video_path)
        
        try:
            # Load audio clip
            audio_clip = mp.AudioFileClip(audio_path)
            
            # Set audio for video clip
            video_clip = video_clip.set_audio(audio_clip)
            
            # Write combined clip to file
            combined_clip_path = os.path.join(output_dir, f"combined_clip_{i}.mp4")
            video_clip.write_videofile(combined_clip_path, codec='libx264', audio_codec='aac')
            
            print(f"Combined clip {i} successfully created.")
        except Exception as e:
            print(f"Error combining audio and video for clip {i}: {e}")
        
        # Remove both video and audio clips
        os.remove(video_path)
        os.remove(audio_path)
           


def select_video_file():
    """
        Open a file dialog to select the input video file and update the corresponding entry field.
    """
    file_path = filedialog.askopenfilename()
    if file_path:
        video_entry.delete(0, tk.END)
        video_entry.insert(0, file_path)

def select_output_directory():
    """
        Open a directory dialog to select the output directory and update the corresponding entry field.
    """
    output_dir = filedialog.askdirectory()
    if output_dir:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_dir)

def segment_video():
    """
        Segment the input video into clips based on shot boundaries and save the segmented clips.
    """
    video_path = video_entry.get()
    output_dir = output_entry.get()
    
    if not video_path or not output_dir:
        messagebox.showerror("Error", "Please select both video file and output directory")
        return
    
    threshold = 0.32  # You may change the threshold according to the video
    boundaries = shot_boundary_detection(video_path, threshold)
    
    if boundaries:
        clip_video(video_path, boundaries, output_dir)
        clip_audio(video_path, boundaries, output_dir)
        combine_video_audio(output_dir, output_dir, output_dir)
        messagebox.showinfo("Success", "All clips are segmented and combined successfully")
    else:
        messagebox.showinfo("Info", "No shot boundaries found")

def on_closing():
    """
        Handle the closing of the application window and prompt the user for confirmation.
    """
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

def show_help():
    """
        Display help information about the video segmentation tool.
    """
    messagebox.showinfo("Help", "This is a video segmentation tool. Select a video file and an output directory, then click 'Segment Video' to segment the video into clips based on shot boundaries.")


"""
    Create the graphical user interface for the video segmentation tool using tkinter library
"""
root = tk.Tk()
root.title("Video Segmentation Tool")
root.geometry("621x400")

style = ttk.Style()
style.configure('TButton', font=('calibri', 10, 'bold'), foreground='black', background='#ffc107')
style.configure('TLabel', font=('calibri', 12))

video_label = ttk.Label(root, text="Select Video File:")
video_label.pack()

video_entry = ttk.Entry(root, width=50)
video_entry.pack()

video_button = ttk.Button(root, text="Browse", command=select_video_file)
video_button.pack()

output_label = ttk.Label(root, text="Select Output Directory:")  # Corrected line
output_label.pack()

output_entry = ttk.Entry(root, width=50)
output_entry.pack()

output_button = ttk.Button(root, text="Browse", command=select_output_directory)
output_button.pack()

segment_button = ttk.Button(root, text="Segment Video", command=segment_video)
segment_button.pack()

help_button = tk.Button(root, text="?", font=('calibri', 10), width=2, height=1, command=show_help, bd=0, bg='#ffc107', fg='black', relief='flat', activebackground='#ffc107', activeforeground='black')
help_button.place(x=570, y=10)

signature_label = ttk.Label(root, text=" An App created by Shubham Laxmikant Deshmukh")
signature_label.pack(side=tk.BOTTOM, pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()



# In[ ]:




