from PIL import Image
import random

def generate_swap_list(width, height, swap_count):
    swap_list = []
    for _ in range(swap_count):
        x1, y1 = random.randint(0, width - 1), random.randint(0, height - 1)
        x2, y2 = random.randint(0, width - 1), random.randint(0, height - 1)
        swap_list.append(((x1, y1), (x2, y2)))
    return swap_list

def apply_swaps(pixels, swap_list):
    for (x1, y1), (x2, y2) in swap_list:
        pixels[x1, y1], pixels[x2, y2] = pixels[x2, y2], pixels[x1, y1]

def encrypt_image(image_path, shift, swap_count):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    # Apply arithmetic shift
    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]
            pixels[i, j] = ((r + shift) % 256, (g + shift) % 256, (b + shift) % 256)
    
    # Generate and apply pixel swaps
    swap_list = generate_swap_list(width, height, swap_count)
    apply_swaps(pixels, swap_list)

    # Save swap list for decryption
    with open("swap_list.txt", "w") as f:
        for swap in swap_list:
            f.write(f"{swap}\n")

    img.save("encrypted_image.png")
    print("Image encrypted and saved as 'encrypted_image.png'")

def decrypt_image(image_path, shift, swap_count):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    # Read swap list for decryption
    with open("swap_list.txt", "r") as f:
        swap_list = [eval(line.strip()) for line in f]

    # Reverse the swaps
    apply_swaps(pixels, reversed(swap_list))

    # Apply arithmetic reverse shift
    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]
            pixels[i, j] = ((r - shift) % 256, (g - shift) % 256, (b - shift) % 256)
    
    img.save("decrypted_image.png")
    print("Image decrypted and saved as 'decrypted_image.png'")

def main():
    while True:
        choice = input("Do you want to (E)ncrypt or (D)ecrypt an image? (E/D): ").upper()
        if choice not in ['E', 'D']:
            print("Invalid choice. Please choose 'E' for encryption or 'D' for decryption.")
            continue
        
        image_path = input("Enter the path of the image: ")
        shift = int(input("Enter the shift value: "))
        swap_count = int(input("Enter the number of pixel swaps: "))

        if choice == 'E':
            encrypt_image(image_path, shift, swap_count)
        else:
            decrypt_image(image_path, shift, swap_count)

        if input("Process another image? (Y/N): ").upper() == 'N':
            break

if __name__ == "__main__":
    main()
