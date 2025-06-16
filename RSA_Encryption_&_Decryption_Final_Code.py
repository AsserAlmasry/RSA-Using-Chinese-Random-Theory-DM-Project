import customtkinter as ctk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt

def mod_exp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def is_prime(n, k=5):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True

    d = n - 1
    while d % 2 == 0:
        d //= 2

    for _ in range(k):
        a = 2 + random.randint(0, n - 4)
        x = mod_exp(a, d, n)
        if x == 1 or x == n - 1:
            continue
        prime = False
        while d != n - 1:
            x = (x * x) % n
            d *= 2
            if x == 1:
                return False
            if x == n - 1:
                prime = True
                break
        if not prime:
            return False
    return True

# Function to compute the greatest common divisor
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Function to find the modular inverse
def mod_inverse(e, phi):
    m0, x0, x1 = phi, 0, 1
    while e > 1:
        q = e // phi
        phi, e = e % phi, phi
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

# Function to generate a prime number
def generate_prime(bit_length):
    while True:
        prime = random.getrandbits(bit_length)
        if is_prime(prime):
            return prime

# Function to encrypt a message
def encrypt(message, e, n):
    return mod_exp(message, e, n)

# Function to decrypt a message
def decrypt(encrypted_message, d, n):
    return mod_exp(encrypted_message, d, n)

# Function to handle encryption
def encrypt_message():
    try:
        message = entry_message.get()
        message_chunks = [int(message[i:i+chunk_size]) for i in range(0, len(message), chunk_size)]
        encrypted_chunks = [encrypt(chunk, e, n) for chunk in message_chunks]
        encrypted_message = ' '.join(map(str, encrypted_chunks))
        label_encrypted.configure(text=f"Encrypted message: {encrypted_message}")
        encrypted_map[encrypted_message] = message
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer message")

# Function to handle decryption
def decrypt_message():
    try:
        encrypted_message = entry_encrypted.get()
        encrypted_chunks = list(map(int, encrypted_message.split()))
        decrypted_chunks = [decrypt(chunk, d, n) for chunk in encrypted_chunks]
        decrypted_message = ''.join(map(str, decrypted_chunks))
        label_decrypted.configure(text=f"Decrypted message: {decrypted_message}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer encrypted message")

# Function to plot RSA analysis
def plot_rsa_analysis(p, q, e, d, n):
    plt.figure(figsize=(10, 6))

    # Plotting prime numbers p and q
    plt.subplot(2, 2, 1)
    plt.title('Prime Numbers (p and q)')
    plt.scatter(['p', 'q'], [p, q], color='blue')
    plt.ylabel('Value')
    for i, txt in enumerate([f"p = {p}", f"q = {q}"]):
        plt.annotate(txt, (['p', 'q'][i], [p, q][i]), xytext=(-15, 10), textcoords='offset points')

    # Plotting public and private keys (e and d)
    plt.subplot(2, 2, 2)
    plt.title('Public and Private Keys (e and d)')
    plt.scatter(['Public Key (e)', 'Private Key (d)'], [e, d], color='green')
    plt.ylabel('Value')
    for i, txt in enumerate([f"e = {e}", f"d = {d}"]):
        plt.annotate(txt, (['Public Key (e)', 'Private Key (d)'][i], [e, d][i]), xytext=(-20, 10), textcoords='offset points')

    # Plotting modulus n
    plt.subplot(2, 2, 3)
    plt.bar(['n'], [n], color='red')
    plt.ylabel('Value')
    plt.annotate(f"n = {n}", ('n', n), xytext=(-15, 10), textcoords='offset points')

    plt.tight_layout()
    plt.show()

# Function to handle the plotting button click
def show_keys():
    plot_rsa_analysis(p, q, e, d, n)

# Seed the random number generator
random.seed()

# Generate RSA keys
bit_length = 10  # Adjust the bit length for prime generation as needed

p = generate_prime(bit_length)
q = generate_prime(bit_length)
n = p * q
phi = (p - 1) * (q - 1)
e = 2
while gcd(e, phi) != 1:
    e += 1
d = mod_inverse(e, phi)

# Determine the chunk size
chunk_size = len(str(n)) - 1

# Dictionary to store encrypted messages and their original values
encrypted_map = {}

# Initialize the application
app = ctk.CTk()

# Set the theme (optional)
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

app.title("RSA Encryption and Decryption")

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label_message = ctk.CTkLabel(master=frame, text="Enter message: (integers) ")
label_message.grid(row=0, column=0, pady=10, padx=10)
entry_message = ctk.CTkEntry(master=frame)
entry_message.grid(row=0, column=1, pady=10, padx=10)
button_encrypt = ctk.CTkButton(master=frame, text="Encrypt", command=encrypt_message)
button_encrypt.grid(row=0, column=2, pady=10, padx=10)
label_encrypted = ctk.CTkLabel(master=frame, text="")
label_encrypted.grid(row=1, column=0, columnspan=3, pady=10, padx=10)

label_encrypted_entry = ctk.CTkLabel(master=frame, text="Enter encrypted message:")
label_encrypted_entry.grid(row=2, column=0, pady=10, padx=10)
entry_encrypted = ctk.CTkEntry(master=frame)
entry_encrypted.grid(row=2, column=1, pady=10, padx=10)
button_decrypt = ctk.CTkButton(master=frame, text="Decrypt", command=decrypt_message)
button_decrypt.grid(row=2, column=2, pady=10, padx=10)
label_decrypted = ctk.CTkLabel(master=frame, text="")
label_decrypted.grid(row=3, column=0, columnspan=3, pady=10, padx=10)

button_show_keys = ctk.CTkButton(master=frame, text="Show Keys", command=show_keys)
button_show_keys.grid(row=4, column=0, columnspan=3, pady=10, padx=10)

app.mainloop()
