import sys
import cv2
import numpy as np
import mediapipe as mp

from AppKit import NSApp, NSApplicationActivationPolicyAccessory, NSScreen
from Cocoa import NSWindow, NSBackingStoreBuffered, NSApplication, NSMakeRect, NSColor, NSImageView, NSImage, NSData
from PyObjCTools import AppHelper
from PIL import Image

# ✅ FIXED: TransparentOverlay rewritten properly
class TransparentOverlay:
    def __init__(self):
        screen_frame = NSScreen.mainScreen().frame()
        rect = NSMakeRect(0, 0, screen_frame.size.width, screen_frame.size.height)

        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            rect, 0, NSBackingStoreBuffered, False
        )
        self.window.setLevel_(1000)
        self.window.setOpaque_(False)
        self.window.setBackgroundColor_(NSColor.clearColor())
        self.window.setIgnoresMouseEvents_(True)
        self.window.setAlphaValue_(1.0)
        self.window.orderFrontRegardless()

        self.image_view = NSImageView.alloc().initWithFrame_(rect)
        self.window.contentView().addSubview_(self.image_view)

    def update_image(self, img_bgr):
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb).convert("RGBA")
        data = pil_img.tobytes("raw", "RGBA")
        ns_img = NSImage.alloc().initWithData_(
            NSData.dataWithBytes_length_(data, len(data))
        )
        self.image_view.setImage_(ns_img)

# ---- Face Mesh & Concentration Logic ----
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)

def estimate_concentration(landmarks, w):
    nose_tip = landmarks[1]
    left_eye = landmarks[33]
    right_eye = landmarks[263]
    x_nose = int(nose_tip.x * w)
    x_left = int(left_eye.x * w)
    x_right = int(right_eye.x * w)
    face_center = (x_left + x_right) // 2
    offset = abs(x_nose - face_center)
    max_offset = w // 10
    concentration = max(0, 100 - (offset / max_offset) * 100)
    return int(concentration)

def draw_focus_bar(img, score, x=30, y=60, width=300, height=25):
    bar_color = (0, 165, 255)  # light orange
    border_color = (0, 255, 0)  # green
    bar_w = int((score / 100) * width)
    cv2.rectangle(img, (x, y), (x + width, y + height), border_color, 2)
    cv2.rectangle(img, (x, y), (x + bar_w, y + height), bar_color, -1)
    cv2.putText(img, f"{score}%", (x + width + 10, y + height - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, border_color, 2)

# ---- Main App Runner ----
def run_overlay_app():
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
    overlay = TransparentOverlay()

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        overlay_img = np.zeros_like(frame, dtype=np.uint8)
        concentration = 0

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=overlay_img,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=drawing_spec,
                    connection_drawing_spec=drawing_spec
                )
                concentration = estimate_concentration(face_landmarks.landmark, w)

        draw_focus_bar(overlay_img, concentration)
        overlay.update_image(overlay_img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# ---- App Entry Point ----
if __name__ == "__main__":
    run_overlay_app()
    AppHelper.runEventLoop()
