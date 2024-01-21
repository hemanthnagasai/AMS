import os
import cv2
import face_recognition

def post_attendance(name):
    # Placeholder function to post attendance
    print(f"Attendance posted for {name}")
def compare_images(input_image_path, captured_frames_directory):
    # Load the input image for comparison
    input_image = face_recognition.load_image_file(input_image_path)
    face_locations = face_recognition.face_locations(input_image)
    input_encoding = face_recognition.face_encodings(input_image, face_locations)

    if not input_encoding:
        print("No face found in the input image.")
        return None

    print("Input face encodings:")
    print(input_encoding)

    # Iterate through the captured frames directory
    for filename in os.listdir(captured_frames_directory):
        if filename.endswith(".png"):
            captured_frame_path = os.path.join(captured_frames_directory, filename)

            # Load the captured frame for comparison
            captured_frame = face_recognition.load_image_file(captured_frame_path)
            captured_face_locations = face_recognition.face_locations(captured_frame)
            captured_encoding = face_recognition.face_encodings(captured_frame, captured_face_locations)

            if not captured_encoding:
                print(f"No face found in {captured_frame_path}. Skipping.")
                continue

            print(f"Captured face encodings:")
            print(captured_encoding)

            # Compare face encodings using face_recognition library
            matches = face_recognition.compare_faces(input_encoding, captured_encoding[0], tolerance=0.6)

            if any(matches):
                print(f"Match found! Image path: {captured_frame_path}")

                # Extract the name from the filename (you may need to adjust this based on your naming convention)
                name = os.path.splitext(os.path.basename(captured_frame_path))[0]

                # Post attendance
                post_attendance(name)

                return captured_frame_path

    print("No matching face found in captured frames.")
    return None

 
if __name__ == "__main__":
    image_path = "C:/Users/HP/Desktop/frame_2.png"
    captured_frames_directory = "C:/Users/HP/Desktop/captured_frames"

    result = compare_images(image_path, captured_frames_directory)

    if result:
        print(f"Result: {result}")
    else:
        print("No match found.")
