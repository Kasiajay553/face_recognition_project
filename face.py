import cv2
import face_recognition
from my_face_module import load_known_faces

# Load known faces and names
known_face_encodings, known_face_names = load_known_faces()

# Open the webcam (0 = default webcam)
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Error: Webcam not detected.")
    exit()

while True:
    # Read a frame from the webcam
    ret, frame = video_capture.read()
    if not ret:
        break

    # Resize frame for faster processing (1/4 size)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert image to RGB (face_recognition uses RGB)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect face locations and face encodings
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Loop through faces in the current frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare current face to known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # Use the known face with the smallest distance if match found
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = face_distances.argmin() if face_distances.size > 0 else -1

        if best_match_index != -1 and matches[best_match_index]:
            name = known_face_names[best_match_index]

        # Scale back up face locations
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw label below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    # Display the frame
    cv2.imshow("Face Recognition", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
video_capture.release()
cv2.destroyAllWindows()
