import cv2

# Initialize the camera (0 for default camera)
cap = cv2.VideoCapture(0)

# Set video codec (XVID in this case)
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# Get the default frame width and height
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Create a VideoWriter object for saving the video
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (frame_width, frame_height))

# Initialize variables
recording = False
brightness = 50  # Default brightness value
contrast = 50  # Default contrast value

def adjust_brightness_contrast(frame, brightness=50, contrast=50):
    """Adjust brightness and contrast of the frame."""
    brightness = (brightness - 50) * 2  # Normalize between -100 and 100
    contrast = (contrast - 50) * 2  # Normalize between -100 and 100
    frame = cv2.convertScaleAbs(frame, alpha=1 + contrast / 100, beta=brightness)
    return frame

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Apply brightness and contrast adjustment
    frame = adjust_brightness_contrast(frame, brightness, contrast)

    # If in recording mode, save the frame
    if recording:
        out.write(frame)
        # Show a red circle indicating recording mode
        cv2.circle(frame, (50, 50), 20, (0, 0, 255), -1)

    # Display the current frame
    cv2.imshow('Video Recorder', frame)

    # Keyboard controls
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC to quit
        break
    elif key == 32:  # Space to toggle between preview and record modes
        recording = not recording
    elif key == ord('b'):  # Increase brightness
        brightness = min(100, brightness + 10)
    elif key == ord('n'):  # Decrease brightness
        brightness = max(0, brightness - 10)
    elif key == ord('c'):  # Increase contrast
        contrast = min(100, contrast + 10)
    elif key == ord('v'):  # Decrease contrast
        contrast = max(0, contrast - 10)

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
