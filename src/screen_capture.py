import mss
import mss.tools

def capture_screen_region():
    """Captures a predefined region of the screen and saves it as screenshot.png."""
    try:
        with mss.mss() as sct:
            # Define the capture region (adjust as needed)
            monitor = {"top": 100, "left": 100, "width": 500, "height": 400}

            # Capture the screen region
            sct_img = sct.grab(monitor)

            # Save the image
            mss.tools.to_png(sct_img.rgb, sct_img.size, output="screenshot.png")
            print("Screenshot saved as screenshot.png")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    capture_screen_region()
