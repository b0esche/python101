import qrcode

def generate_qr(data, filename='qr_code.png'):
    """
    Generate a QR code for the given data and save it as an image.
    Requires the 'qrcode' library: pip install qrcode[pil]
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"QR code saved as {filename}")

# Example usage
if __name__ == "__main__":
    generate_qr('https://www.example.com', 'example_qr.png')