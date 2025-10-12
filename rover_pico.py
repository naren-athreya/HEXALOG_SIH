from machine import Pin, PWM, I2C
import time

# =========================
# Motor Driver Setup (TB6612FNG)
# =========================
AIN1 = Pin(2, Pin.OUT)
AIN2 = Pin(3, Pin.OUT)
PWMA = PWM(Pin(4))

BIN1 = Pin(6, Pin.OUT)
BIN2 = Pin(7, Pin.OUT)
PWMB = PWM(Pin(8))

STBY = Pin(9, Pin.OUT)

PWMA.freq(1000)
PWMB.freq(1000)

# Default speed (percentage of full duty cycle)
DEFAULT_SPEED_PERCENT = 60
DEFAULT_SPEED = int(DEFAULT_SPEED_PERCENT * 65535 // 100)


# =========================
# Motor Control Functions
# =========================
def motorA(direction, speed=DEFAULT_SPEED):
    """Control Motor A"""
    if direction == "f":
        AIN1.on()
        AIN2.off()
        PWMA.duty_u16(speed)
    elif direction == "b":
        AIN1.off()
        AIN2.on()
        PWMA.duty_u16(speed)
    else:
        AIN1.off()
        AIN2.off()
        PWMA.duty_u16(0)


def motorB(direction, speed=DEFAULT_SPEED):
    """Control Motor B"""
    if direction == "f":
        BIN1.on()
        BIN2.off()
        PWMB.duty_u16(speed)
    elif direction == "b":
        BIN1.off()
        BIN2.on()
        PWMB.duty_u16(speed)
    else:
        BIN1.off()
        BIN2.off()
        PWMB.duty_u16(0)


def stop():
    """Stop both motors"""
    motorA("s")
    motorB("s")
    print("Motors stopped")


# Enable motor driver and ensure motors are stopped initially
STBY.on()
stop()


# =========================
# MPU6050 Setup
# =========================
i2c = I2C(0, scl=Pin(1), sda=Pin(0))  # GP1=SCL, GP0=SDA
MPU_ADDR = 0x68

# Wake up the MPU6050 (exit sleep mode)
try:
    i2c.writeto_mem(MPU_ADDR, 0x6B, b'\x00')
except Exception as e:
    print("MPU6050 not detected:", e)


def read_mpu6050():
    """Read accelerometer values from MPU6050"""
    try:
        data = i2c.readfrom_mem(MPU_ADDR, 0x3B, 6)
        accel_x = int.from_bytes(data[0:2], 'big', signed=True)
        accel_y = int.from_bytes(data[2:4], 'big', signed=True)
        accel_z = int.from_bytes(data[4:6], 'big', signed=True)
        return accel_x, accel_y, accel_z
    except Exception as e:
        print("MPU6050 read error:", e)
        return None, None, None


# =========================
# Main Control Loop
# =========================
print("Rover ready. Enter commands:")
print("f = forward, b = back, l = left, r = right, s = stop")

try:
    while True:
        cmd = input("Enter command: ").lower()

        try:
            # Motor commands
            if cmd == "f":
                motorA("f")
                motorB("f")
                print("Moving forward")
            elif cmd == "b":
                motorA("b")
                motorB("b")
                print("Moving backward")
            elif cmd == "l":
                motorA("b")
                motorB("f")
                print("Turning left")
            elif cmd == "r":
                motorA("f")
                motorB("b")
                print("Turning right")
            elif cmd == "s":
                stop()
            else:
                print("Invalid command. Use f, b, l, r, or s.")

            # Read MPU6050 values
            ax, ay, az = read_mpu6050()
            if ax is not None:
                print(f"MPU6050 -> X: {ax}, Y: {ay}, Z: {az}")

        except Exception as e:
            print("Error executing command:", e)
            stop()

except KeyboardInterrupt:
    stop()
    print("Program stopped by user")
