import requests
import firebase_admin
from firebase_admin import credentials, storage
from flask import Flask, jsonify

# Khởi tạo Firebase Admin SDK
cred = credentials.Certificate("F:/EoH Company/Capture_Image_iFrame/firebase/pythoncodeCaptureIMG_Camera/captureimage-38a12-firebase-adminsdk-ngvh0-d868c69238.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'captureimage-38a12.appspot.com'  #projectID
})

def capture_and_upload_image():
    try:
        # Tải ảnh từ HIKVISION
        url = "http://admin:Eoh54321@14.241.233.207:28001/ISAPI/Streaming/channels/1/picture"
        response = requests.get(url, timeout=10)

        # In trạng thái phản hồi
        print("HTTP Status Code từ camera:", response.status_code)
        
        if response.status_code == 200:
            # Tải ảnh lên Firebase Storage
            bucket = storage.bucket()
            blob = bucket.blob('images/camera_image.jpg')
            blob.upload_from_string(response.content, content_type='image/jpeg')
            
            # Tạo URL công khai
            blob.make_public()
            print('Public URL:', blob.public_url)
            
            return blob.public_url
        else:
            print("Lỗi khi tải ảnh từ camera:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Lỗi khi kết nối tới camera:", e)
        return None
    except Exception as e:
        print("Lỗi không mong muốn xảy ra:", e)
        return None

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

@app.route('/capture', methods=['GET'])
def capture_image():
    try:
        public_url = capture_and_upload_image()
        if public_url:
            return jsonify({"imageUrl": public_url})
        else:
            return jsonify({"error": "Failed to capture image"}), 500
    except Exception as e:
        print("Lỗi xảy ra trong /capture:", e)
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
