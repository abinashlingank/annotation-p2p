import cv2
import os

parent_dir = 'c'
video_path = parent_dir+'/c.mp4'

# Function to handle mouse events
def mouse_click(event, x, y, flags, param):
    global coordinates
    if event == cv2.EVENT_LBUTTONDOWN:  # Left mouse button clicked
        # Print and save the coordinates
        print(f"Clicked at: ({x}, {y})")
        coordinates.append((x, y))
        # Draw a circle at the clicked point
        cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
        cv2.imshow(window_name, frame)

if not os.path.exists(f'{parent_dir}/annotated-images'):
    os.makedirs(f'{parent_dir}/annotated-images')
# Function to save annotated image
def save_annotated_image(image_name):
    output_filename = os.path.join(f'{parent_dir}/annotated-images', image_name)
    cv2.imwrite(output_filename, frame)
    print(f"Annotated image saved to {output_filename}")


# Function to save coordinates to a text file
if not os.path.exists(f'{parent_dir}/ground-truth-txt'):
    os.makedirs(f'{parent_dir}/ground-truth-txt')
def save_coordinates(image_name, coordinates):
    output_filename = os.path.splitext(image_name)[0] + '.txt'
    output_filename = os.path.join(f'{parent_dir}/ground-truth-txt', output_filename)
    with open(output_filename, 'w') as f:
        for coord in coordinates:
            f.write(f"{coord[0]} {coord[1]}\n")
    print(f"Labels saved to {output_filename}")



file_path = video_path
print(f"Reading video from {file_path}")

# Load the video
if not os.path.exists(f'{parent_dir}/images'):
    os.makedirs(f'{parent_dir}/images')
cap = cv2.VideoCapture(file_path)
frame_no = 1
while True:
    ret, frame = cap.read()
    if not ret:
        if frame_no == 1:
            print("Error: No frames in the video. Exiting.")
        break
    if frame_no % 10 == 0 or frame_no == 1:  # Process every 10th frame
        coordinates = []
        window_name = f'frame_{frame_no-1}'
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, mouse_click)
        cv2.imshow(window_name, frame)
        file_name = f'IMG_{frame_no-1}.jpg'
        cv2.imwrite(os.path.join(f'{parent_dir}/images', file_name), frame)
        print(f"Image saved to {parent_dir}/images", file_name)
        print("Click on the image to select points. Press 'd' when done.")
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('d'):  # 'd' key pressed (done)
                save_coordinates(file_name, coordinates)
                save_annotated_image(file_name)
                cv2.destroyWindow(window_name)
                break
    frame_no += 1

# Release video capture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
