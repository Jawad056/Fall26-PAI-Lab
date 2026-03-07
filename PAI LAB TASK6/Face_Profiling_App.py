import os
import cv2
from flask import Flask, render_template, request

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/output'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load Haar cascade files from OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    output_image = None

    if request.method == 'POST':
        file = request.files['image']

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            image = cv2.imread(filepath)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            face_count = len(faces)
            eye_count_total = 0
            measurements = []

            for i, (x, y, w, h) in enumerate(faces, start=1):
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                roi_gray = gray[y:y+h, x:x+w]
                roi_color = image[y:y+h, x:x+w]

                eyes = eye_cascade.detectMultiScale(roi_gray)
                eye_count_total += len(eyes)

                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)

                measurements.append({
                    'face_number': i,
                    'width': w,
                    'height': h,
                    'eyes_detected': len(eyes)
                })

            output_filename = 'processed_' + file.filename
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            cv2.imwrite(output_path, image)

            if face_count > 0:
                profile = "Face detected successfully. This appears to be a frontal face image."
            else:
                profile = "No clear face detected."

            result = {
                'face_count': face_count,
                'eye_count': eye_count_total,
                'measurements': measurements,
                'profile': profile
            }

            output_image = output_filename

    return render_template('index.html', result=result, output_image=output_image)

if __name__ == '__main__':
    app.run(debug=True)