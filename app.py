from flask import Flask, render_template, request, jsonify
import cv2, os, sqlite3, base64, numpy as np

app = Flask(__name__)

# ========== DATABASE ==========
conn = sqlite3.connect('buspass.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS passengers (id INTEGER PRIMARY KEY, name TEXT)')
conn.commit()

# ========== FACE SETUP ==========
CASCADE_PATH = 'haarcascade_frontalface_default.xml'
if not os.path.exists(CASCADE_PATH):
    raise FileNotFoundError(
        f"{CASCADE_PATH} not found. Download it from "
        "https://github.com/opencv/opencv/tree/master/data/haarcascades "
        "and place it in this folder."
    )

face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
os.makedirs('faces', exist_ok=True)


# ========== UTILITIES ==========
def train_model_auto():
    """Retrains the LBPH model whenever a new face is added."""
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, ids = [], []

    for img_name in os.listdir('faces'):
        if not img_name.lower().endswith('.jpg'):
            continue
        path = os.path.join('faces', img_name)
        gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if gray is None:
            continue
        try:
            id_ = int(img_name.split('.')[1])
        except Exception:
            continue
        faces.append(gray)
        ids.append(id_)

    if len(faces) < 1:
        print("⚠️ Not enough data to train yet.")
        return False

    recognizer.train(faces, np.array(ids))
    recognizer.save('trainer.yml')
    print("✅ Model retrained automatically.")
    return True


def is_duplicate_face(new_face_gray):
    """Checks if a new face already exists using the current model."""
    if not os.path.exists('trainer.yml'):
        return False
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer.yml')
    _, conf = recognizer.predict(new_face_gray)
    return conf < 60


# ========== ROUTES ==========
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/register_from_web', methods=['POST'])
def register_from_web():
    data = request.get_json()
    name = data['name'].strip()
    images = data['images']

    # --- Validate input ---
    if not images or len(images) == 0:
        return jsonify({'message': '⚠️ No images received. Try again.'})

    # --- Duplicate name check ---
    c.execute('SELECT * FROM passengers WHERE LOWER(name)=LOWER(?)', (name,))
    if c.fetchone():
        return jsonify({'message': f'⚠️ {name} is already registered by name!'})

    # --- Insert new passenger ---
    c.execute('INSERT INTO passengers (name) VALUES (?)', (name,))
    uid = c.lastrowid
    conn.commit()

    os.makedirs('faces', exist_ok=True)
    saved_count = 0

    for i, img_data in enumerate(images, start=1):
        img_bytes = base64.b64decode(img_data.split(',')[1])
        npimg = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_crop = gray[y:y + h, x:x + w]
            cv2.imwrite(f'faces/User.{uid}.{saved_count + 1}.jpg', face_crop)
            saved_count += 1
            break  # one face per frame

    if saved_count == 0:
        return jsonify({'message': '⚠️ No faces detected in captured frames. Try again.'})

    # --- Retrain model automatically ---
    train_model_auto()

    return jsonify({'message': f'{name} registered successfully with {saved_count} samples! Model updated.'})


@app.route('/validate')
def validate_page():
    return render_template('validate.html')


@app.route('/validate_from_web', methods=['POST'])
def validate_from_web():
    data = request.get_json()
    img_data = data['image'].split(',')[1]
    npimg = np.frombuffer(base64.b64decode(img_data), np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if not os.path.exists('trainer.yml'):
        return jsonify({'message': '⚠️ Model not trained yet. Register at least one passenger.'})
    if len(faces) == 0:
        return jsonify({'message': '⚠️ No face detected. Please face the camera clearly.'})

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer.yml')

    best_match, best_conf = None, 999
    for (x, y, w, h) in faces:
        id_, conf = recognizer.predict(gray[y:y+h, x:x+w])
        print(f"[DEBUG] ID={id_}, conf={conf:.2f}")
        if conf < best_conf:
            best_conf, best_match = conf, id_

    if best_conf < 55:
        c.execute('SELECT name FROM passengers WHERE id=?', (best_match,))
        user = c.fetchone()
        if user:
            return jsonify({'message': f'✅ Pass Validated: {user[0]} (confidence {best_conf:.1f})'})
        return jsonify({'message': '❌ Record missing for recognized face.'})
    elif best_conf < 80:
        return jsonify({'message': f'⚠️ Partial match (confidence {best_conf:.1f}). Try again or adjust lighting.'})
    else:
        return jsonify({'message': '❌ Face not recognized. Please buy ticket manually or via scanner.'})


# ========== RUN ==========
if __name__ == '__main__':
    app.run(debug=True)