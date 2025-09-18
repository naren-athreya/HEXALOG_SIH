import cv2
import time
import board
import busio
import adafruit_mlx90614

# i2c setup for MLX90614
i2c = busio.I2C(board.SCL, board.SDA)
mlx = adafruit_mlx90614.MLX90614(i2c)

# camera setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Camera not found")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    temp = mlx.object_temperature
    text = f"Temp: {temp:.2f} C"
    cv2.putText(frame, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("AI Vision Rover Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
