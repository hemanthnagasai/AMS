import cv2
from PIL import Image, ImageDraw, ImageGrab
import numpy as np
import face_recognition
import time
import os

classNames = ['Person1', 'Person2', 'Person3']

def findEncodings(images):
    encodeList = []
    for img in images:
        encodings = face_recognition.face_encodings(np.array(img))
        if encodings:
            encodeList.append(encodings[0])
    return encodeList

def process_frame(frame_rgb, encodeListKnown, draw):
    frame_pil = Image.fromarray(frame_rgb)
    faces_cur_frame = face_recognition.face_locations(np.array(frame_pil))
    encodes_cur_frame = face_recognition.face_encodings(np.array(frame_pil), faces_cur_frame)

    for encode_face, face_loc in zip(encodes_cur_frame, faces_cur_frame):
        matches = face_recognition.compare_faces(encodeListKnown, encode_face)
        face_dis = face_recognition.face_distance(encodeListKnown, encode_face)

        if face_dis.size > 0:
            match_index = np.argmin(face_dis)
            y1, x2, y2, x1 = face_loc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            if matches[match_index]:
                name = classNames[match_index].upper()
                draw.rectangle([(x1, y1), (x2, y2)], outline=(0, 255, 0), width=2)
                draw.rectangle([(x1, y2 - 35), (x2, y2)], fill=(0, 255, 0))
                draw.text((x1 + 6, y2 - 6), name, font=None, fill=(255, 255, 255), anchor="start")
            else:
                draw.rectangle([(x1, y1), (x2, y2)], outline=(0, 0, 255), width=2)
                draw.rectangle([(x1, y2 - 35), (x2, y2)], fill=(0, 0, 255))
                draw.text((x1 + 6, y2 - 6), 'Stranger', font=None, fill=(255, 255, 255), anchor="start")
                print('Unknown Face')

    return frame_pil

def capture_frame():
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cap.release()
        return frame_rgb, True
    except Exception as e:
        print(f"Error capturing frame: {e}")
        return None, False

output_directory = "captured_frames"
os.makedirs(output_directory, exist_ok=True)

initial_frame_rgb, success = capture_frame()

if success and initial_frame_rgb is not None:
    try:
        encodeListKnown = findEncodings([initial_frame_rgb])
        print('Encoding Complete')

        frame_limit = 3
        frame_count = 0
        draw = ImageDraw.Draw(Image.fromarray(initial_frame_rgb))

        while frame_count < frame_limit:
            current_frame_rgb, success = capture_frame()

            if success and current_frame_rgb is not None:
                processed_frame = process_frame(current_frame_rgb, encodeListKnown, draw)
                draw = ImageDraw.Draw(processed_frame)
                processed_frame.show()  # You can replace this line with saving to a file
                frame_count += 1

                # Save the processed frame as an image
                output_path = os.path.join(output_directory, f"frame_{frame_count}.png")
                processed_frame.save(output_path)
                print(f"Processed frame saved to {output_path}")
            else:
                print('Invalid frame - skipping')
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print('Invalid initial frame - exiting')
