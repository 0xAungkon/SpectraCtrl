from pynput import mouse, keyboard
import time

def control_input():
    """Demonstrates basic mouse and keyboard control using pynput."""
    try:
        mouse_controller = mouse.Controller()
        keyboard_controller = keyboard.Controller()

        # Mouse control
        target_position = (100, 200)
        mouse_controller.position = target_position
        print(f"Mouse moved to {target_position}")
        time.sleep(0.1) # Adding a small delay to ensure action completes

        mouse_controller.click(mouse.Button.left)
        print("Mouse left-clicked")
        time.sleep(0.1)

        # Keyboard control
        text_to_type = "Hello from pynput!"
        keyboard_controller.type(text_to_type)
        print(f"Typed: '{text_to_type}'")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    control_input()
