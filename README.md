# Face Recognition Bus Pass Validation (Modern UI)

## Quick start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Important:** download `haarcascade_frontalface_default.xml` from OpenCV's GitHub:
   https://github.com/opencv/opencv/tree/master/data/haarcascades
   Place the file in the project root.

3. Run:
   ```bash
   python app.py
   ```

4. Open http://127.0.0.1:5000 and use the app.

## Notes
- Trainer file `trainer.yml` is generated after running Train System.
- Captured face images are stored in `faces/`.
