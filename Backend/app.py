import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import matplotlib.pyplot as plt
import numpy as np
from deepface import DeepFace

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
GRAPH_FOLDER = 'graphs'
FRAME_FOLDER = 'frames'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(GRAPH_FOLDER):
    os.makedirs(GRAPH_FOLDER)
if not os.path.exists(FRAME_FOLDER):
    os.makedirs(FRAME_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_video():
    file = request.files['file']
    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    cap = cv2.VideoCapture(file_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    detected_emotions = []
    time_stamps = []  
    frame_emotions = []
    frame_previews = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  
        frame_count += 1
        time_in_seconds = frame_count / fps

        if frame_count % 30 == 0:
            try:
                result = DeepFace.analyze(frame, actions=['emotion'], detector_backend='mtcnn', enforce_detection=False)
                dominant_emotion = result[0]['dominant_emotion'] if isinstance(result, list) else result['dominant_emotion']
                detected_emotions.append(dominant_emotion)
                time_stamps.append(time_in_seconds)
                frame_emotions.append({"time": time_in_seconds, "emotion": dominant_emotion})

                # Save the current frame as an image and return its path
                frame_filename = f"{filename}_frame_{frame_count}.jpg"
                frame_path = os.path.join(FRAME_FOLDER, frame_filename)
                cv2.imwrite(frame_path, frame)
                frame_previews.append(f"http://localhost:5000/frame/{frame_filename}")
            except Exception as e:
                detected_emotions.append('error')
                time_stamps.append(time_in_seconds)
                frame_emotions.append({"time": time_in_seconds, "emotion": "error"})
                frame_previews.append(None)

    cap.release()

    # Generate the graph
    emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    emotion_to_num = {emotion: idx for idx, emotion in enumerate(emotion_labels)}
    emotion_numbers = [emotion_to_num.get(emotion, np.nan) for emotion in detected_emotions]

    plt.figure(figsize=(12, 6))
    plt.plot(time_stamps, emotion_numbers, marker='o')
    plt.yticks(ticks=range(len(emotion_labels)), labels=emotion_labels)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Emotion')
    plt.title('Time vs Emotion Graph')
    plt.grid(True)

    graph_name = f"{filename}_emotion_graph.png"
    graph_path = os.path.join(GRAPH_FOLDER, graph_name)
    plt.savefig(graph_path)
    plt.close()

    return jsonify({
        "message": "success",
        "frame_emotions": frame_emotions,
        "frames": frame_previews,
        "graph_name": graph_name
    })

@app.route('/graph/<filename>')
def get_graph(filename):
    return send_from_directory(GRAPH_FOLDER, filename)

@app.route('/frame/<filename>')
def get_frame(filename):
    return send_from_directory(FRAME_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)