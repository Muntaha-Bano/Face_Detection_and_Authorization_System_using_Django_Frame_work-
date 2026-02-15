import json
import base64
import uuid
import os
from pathlib import Path
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import cv2
import numpy as np
from django.http import StreamingHttpResponse
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    return render(request, 'face_verification/home.html')

def signup(request):
    return render(request, 'face_verification/signup.html')

def face_login(request):
    return render(request, 'face_verification/login.html')

import uuid
from .services.face_services import register_face, recognize_face

output_dir = Path('FACE_RECOGNIZATION/faceID_Bot/face_verification/face_images')
output_dir.mkdir(parents=True, exist_ok=True)

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml'
)

temp_captured_image = None
temp_face_path = None
captured_frame_base64 = None


def gen_frames():
    """Generate frames for video streaming"""
    cap = cv2.VideoCapture(0)
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        # Detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        
        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()
    
def video_feed(request):
    """Video streaming route"""
    return StreamingHttpResponse(
        gen_frames(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

@csrf_exempt
def capture_face(request):
    """Capture and save a face image from canvas (original function - keep for compatibility)"""
    if request.method == 'POST':
        try:
            # Get image data from request
            data = json.loads(request.body)
            image_data = data.get('image')
            
            # Decode base64 image
            image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Detect face
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            if len(faces) > 0:
                # Get the first face
                (x, y, w, h) = faces[0]
                face_img = frame[y:y+h, x:x+w]
                
                # Count existing faces
                existing_faces = len(list(output_dir.glob('face_*.jpg')))
                
                # Save face
                face_path = output_dir / f"face_{existing_faces:03d}.jpg"
                cv2.imwrite(str(face_path), face_img)
                
                return JsonResponse({
                    'success': True,
                    'message': 'Face captured successfully!',
                    'count': existing_faces + 1
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'No face detected. Please position your face in the frame.'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def capture_face_from_camera(request):
    """Capture face directly from camera with registration support"""
    global temp_face_path, captured_frame_base64
    
    if request.method == 'POST':
        try:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                return JsonResponse({
                    'success': False,
                    'message': 'Could not access camera'
                })
            
            # Read frame
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                return JsonResponse({
                    'success': False,
                    'message': 'Could not capture frame'
                })
            
            # Detect face
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            if len(faces) > 0:
                # Get the first face
                (x, y, w, h) = faces[0]
                face_img = frame[y:y+h, x:x+w]
                
                # Generate unique filename
                face_filename = f"temp_face_{uuid.uuid4().hex[:8]}.jpg"
                temp_face_path = output_dir / face_filename
                
                # Save face temporarily
                cv2.imwrite(str(temp_face_path), face_img)

                # Build an image that contains only the detected face region
                # (rest of the image will be black). This ensures the frontend
                # renders the captured frame only on the face area, not the
                # entire body/frame.
                masked_frame = np.zeros_like(frame)
                masked_frame[y:y+h, x:x+w] = face_img

                # Encode masked frame to base64 for display
                _, buffer = cv2.imencode('.jpg', masked_frame)
                captured_frame_base64 = base64.b64encode(buffer).decode('utf-8')
                
                # Count existing registered faces
                existing_faces = len(list(output_dir.glob('registered_face_*.jpg')))
                
                return JsonResponse({
                    'success': True,
                    'message': 'Face captured successfully!',
                    'count': existing_faces + 1,
                    'show_dialog': True,
                    'captured_image': f"data:image/jpeg;base64,{captured_frame_base64}"
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'No face detected. Please position your face in the frame.'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def check_existing_user(request):
    """Check if captured face matches existing user"""
    global temp_face_path
    
    if request.method == 'POST' and temp_face_path:
        try:
            result = recognize_face(str(temp_face_path))
            
            if result['status'] == 'recognized':
                return JsonResponse({
                    'success': True,
                    'recognized': True,
                    'name': result['name'],
                    'score': result['score']
                })
            else:
                return JsonResponse({
                    'success': True,
                    'recognized': False,
                    'message': 'New user detected. Please register.'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Recognition error: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'No face captured yet. Please capture a face first.'
    })

@csrf_exempt
def login_user(request):
    global temp_face_path

    if request.method == 'POST' and temp_face_path:
        try:
            result = recognize_face(str(temp_face_path))

            if result['status'] == 'recognized':
                face_recognized_name = result['name']  # face-recognized name from face_services.py
                print(f"DEBUG - Face recognized as: {face_recognized_name}")

                # Create username from recognized name (normalize for Django)
                username = face_recognized_name.lower().replace(" ", "_")
                print(f"DEBUG - Django username: {username}")

                # Get or create Django user
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={'first_name': face_recognized_name}  # Store original name as first_name
                )
                
                # If user already exists but first_name is different, update it
                if not created and user.first_name != face_recognized_name:
                    user.first_name = face_recognized_name
                    user.save()
                    print(f"DEBUG - Updated user first_name to: {face_recognized_name}")
                
                print(f"DEBUG - Django user: username={user.username}, first_name={user.first_name}, created={created}")

                # Log user into Django session
                django_login(request, user)
                print(f"DEBUG - User logged in: {request.user.username}, first_name={request.user.first_name}")
                
                # Store recognized name in session for chatbot
                request.session['user_name'] = face_recognized_name
                print(f"DEBUG - Session user_name set to: {request.session['user_name']}")

                # Cleanup temp face
                if temp_face_path and temp_face_path.exists():
                    os.remove(str(temp_face_path))
                    temp_face_path = None

                return JsonResponse({
                    'success': True,
                    'recognized': True,
                    'name': face_recognized_name,
                    'score': result['score'],
                    'redirect_url': '/chatbot/'
                })

            else:
                return JsonResponse({
                    'success': True,
                    'recognized': False,
                    'message': 'Face not recognized.'
                })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Authentication error: {str(e)}'
            })

    return JsonResponse({
        'success': False,
        'message': 'No face captured yet.'
    })

@csrf_exempt
def register_user(request):
    """Register user with face and information"""
    global temp_face_path
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Get user information
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            
            if not all([first_name, last_name]):
                return JsonResponse({
                    'success': False,
                    'message': 'Missing information. Please fill all fields.'
                })
            
            if not temp_face_path or not temp_face_path.exists():
                return JsonResponse({
                    'success': False,
                    'message': 'No face captured. Please capture a face first.'
                })
            
            # Generate user ID
            user_id = str(uuid.uuid4())
            
            # Combine first and last names for display
            full_name = f"{first_name} {last_name}"
            
            # Register face using service
            try:
                register_face(str(temp_face_path), user_id, full_name)
                
                # Move temp file to permanent location
                permanent_filename = f"registered_face_{user_id}.jpg"
                permanent_path = output_dir / permanent_filename
                os.rename(str(temp_face_path), str(permanent_path))
                
                # Clean up global variable
                temp_face_path = None
                
                return JsonResponse({
                    'success': True,
                    'message': f'User {full_name} registered successfully!',
                    'user_id': user_id
                })
                
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Registration failed: {str(e)}'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def get_captured_image(request):
    """Get the last captured image (for display)"""
    global captured_frame_base64
    
    if captured_frame_base64:
        return JsonResponse({
            'success': True,
            'image': f"data:image/jpeg;base64,{captured_frame_base64}"
        })
    
    return JsonResponse({
        'success': False,
        'message': 'No image captured yet'
    })
