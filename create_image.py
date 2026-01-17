import base64

# Convert keyboard_image.png to base64
try:
    with open("keyboard_image.png", "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    
    print("Image converted successfully!")
    print("\nCopy the text below and paste it into the _get_embedded_image() method:")
    print("=" * 60)
    print(encoded)
    print("=" * 60)
    
    # Also save to file for easy copying
    with open("image_base64.txt", "w") as f:
        f.write(encoded)
    
    print("\nAlso saved to 'image_base64.txt' for easy copying!")
    
except FileNotFoundError:
    print("ERROR: keyboard_image.png not found in current directory")
except Exception as e:
    print(f"ERROR: {e}")

input("\nPress Enter to close...")