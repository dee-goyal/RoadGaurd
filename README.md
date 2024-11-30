# RoadGuard 🚗  
**Developed by Deepika Goyal**  

RoadGuard is a smart road safety application that uses AI to detect potholes in real-time, alert drivers with a sound, and automatically log complaints for road repairs. It ensures safer travels by addressing road issues proactively.  

---

### Features  
1. **Live Webcam Detection**  
   - Detects potholes in real-time using a webcam.  

2. **Auto File Complaints**  
   - Automatically logs complaints when a pothole is detected, including location and time.  

3. **Beep Alert**  
   - Plays an alert sound when a risky pothole is identified.  

---

### How to Use  
1. **Install Dependencies**  
   - Install the required Python libraries:  
     ```bash  
     pip install -r requirements.txt  
     ```  

2. **Run the Application**  
   - Start the Flask app:  
     ```bash  
     python app.py  
     ```  

3. **Access the App**  
   - Open your browser and navigate to `http://127.0.0.1:5000`.  

4. **Detect Potholes**  
   - Use the live detection feature via webcam.  

---

### Technologies Used  
- Python  
- OpenCV  
- Flask  
- YOLOv3 Tiny  

---

### Project Structure  
```plaintext  
RoadGuard/  
├── static/  
│   ├── alert.mp3  
│   └── styles.css  
├── templates/  
│   ├── index.html  
│   └── complaints.html  
├── project_files/  
│   ├── yolov3_tiny.cfg  
│   └── yolov3_tiny.weights  
├── app.py  
├── requirements.txt  
└── README.md  
```  

---

### Future Enhancements  
- **Rain Detection**: Identify water-filled potholes.  
- **Severity Prediction**: Predict pothole depth and severity more accurately.  
- **Mobile Integration**: Build a mobile app version.  

---

### Screenshots and Demo  
*(Add images or video links here)*  

---

### Author  
Developed with ❤️ by **Deepika Goyal**.
