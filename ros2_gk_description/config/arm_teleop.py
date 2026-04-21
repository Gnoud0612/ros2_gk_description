import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import sys, termios, tty

msg = """
================================
 ĐIỀU KHIỂN CÁNH TAY ROBOT ROS 2
================================
 A / D : Xoay trái / phải  (Arm 1) 
 W / S : Gập lên / xuống (Arm 2)

 Q hoặc Ctrl+C : Thoát chương trình
================================
"""

def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('arm_keyboard_teleop')

    # Kết nối với bộ điều khiển tay máy trong Gazebo
    pub = node.create_publisher(Float64MultiArray, '/arm_controller/commands', 10)
    
    settings = termios.tcgetattr(sys.stdin)
    pos1 = 0.0
    pos2 = 0.0
    step = 0.1  # Chỉnh tốc độ quay
    
    print(msg)

    try:
        while rclpy.ok():
            key = get_key(settings)
            
            # Đọc lệnh từ bàn phím
            if key == 'a':
                pos1 += step   # Arm 1 trái
            elif key == 'd':
                pos1 -= step   # Arm 1 phải
            elif key == 'w':
                pos2 += step   # Arm 2 lên
            elif key == 's':
                pos2 -= step   # Arm 2 xuống
            elif key == '\x03' or key == 'q':  # Thoát
                break
            else:
                continue
            
            # Gửi lệnh xuống Gazebo
            command = Float64MultiArray()
            command.data = [pos1, pos2]
            pub.publish(command)
            
            # Hiển thị trạng thái
            print(f"\r[Trạng thái] Khớp 1: {pos1:.1f} rad | Khớp 2: {pos2:.1f} rad   ", end='')

    except Exception as e:
        print(f"Lỗi: {e}")

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

