import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import qrcode
import tkinter as tk
import math

def main():

    #Variables of the second window (from existing)
    file_path = os.environ.get("file_path")
    output_folder = os.environ.get("output_folder")
    parambig = os.environ.get("parambig")
    paramsmall = os.environ.get("paramsmall")

    if file_path and output_folder and (parambig != '0' or paramsmall != '0'):

        df = pd.read_csv(file_path, header=None)
        # Create a new column containing the character length of each element in the first column
        df['char_length'] = df[0].apply(lambda x: calculate_text_width(x, "Helvetica", 14))
        print(df)

        values = df[0].tolist()

        if parambig == '1':

            # Splitting the values into groups of 80 (number of labels per page)
            value_groups = [values[i:i + 80] for i in range(0, len(values), 80)]

            # Set up the PDF canvas
            pdf_path = output_folder + "/big_labels_generated.pdf"
            pdf = canvas.Canvas(pdf_path, pagesize=A4)

            # Set the dimensions of the labels in centimeters
            label_width_cm = 3.56 * cm
            label_height_cm = 1.69 * cm

            # Set the spacing between labels
            x_spacing = label_width_cm + 0.27 * cm
            y_spacing = label_height_cm

            # Set the initial position for drawing
            x_start = 0.2  * cm
            y_start = A4[1] - 1.33 * cm

            # Iterate over the value groups
            for group in value_groups:
                # Calculate the number of rows and columns needed for this group
                num_rows = (len(group) - 1) // 5 + 1
                num_cols = min(len(group), 5)

                # Calculate the total width and height needed for this group
                total_width = num_cols * x_spacing
                total_height = num_rows * y_spacing

                # Calculate the starting position for this group
                x = x_start + (A4[0] - total_width) / 2
                y = y_start - total_height

                # Iterate over the values in the group
                for i, value in enumerate(group):
                    # Calculate the position for drawing the value and QR code
                    pos_x = x + (i % 5) * x_spacing
                    pos_y = y + (i // 5) * y_spacing

                    if (df['char_length'][i] <= 1.9).any():

                        # Set the font size
                        font_size = 14

                        # Draw the label text
                        pdf.setFont("Helvetica", font_size)
                        pdf.drawString(pos_x + 0.07 * cm, pos_y + 0.8 * cm, value)

                        # Draw the QR code
                        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=13.5, border=0 )
                        qr.add_data(value)
                        qr.make(fit=True)
                        qr_img = qr.make_image(fill_color="black", back_color="white")

                        # Calculate the position for drawing the QR code
                        qr_pos_x = pos_x + 1.9 * cm
                        qr_pos_y = pos_y + 0.2 * cm

                        # Draw the QR code
                        qr_img_path = "qr_code.png"
                        qr_img.save(qr_img_path)
                        pdf.drawInlineImage(qr_img_path, qr_pos_x, qr_pos_y, width=1.35 * cm, height=1.35 * cm)

                    elif (df['char_length'][i] > 1.9 and df['char_length'][i] <= 3.8).any():

                        # Set the font size
                        font_size = 14

                        length = len(value)
                        semi_length = round(length/2)

                        # Draw the label text
                        pdf.setFont("Helvetica", font_size)
                        pdf.drawString(pos_x + 0.07 * cm, pos_y + 1 * cm, value[:semi_length])
                        pdf.setFont("Helvetica", font_size)  # Reduce font size for the second line
                        pdf.drawString(pos_x + 0.07 * cm, pos_y + 0.5 * cm, value[semi_length:])

                        # Draw the QR code
                        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=13.5, border=0 )
                        qr.add_data(value)
                        qr.make(fit=True)
                        qr_img = qr.make_image(fill_color="black", back_color="white")

                        # Calculate the position for drawing the QR code
                        qr_pos_x = pos_x + 1.9 * cm
                        qr_pos_y = pos_y + 0.2 * cm

                        # Draw the QR code
                        qr_img_path = "qr_code.png"
                        qr_img.save(qr_img_path)
                        pdf.drawInlineImage(qr_img_path, qr_pos_x, qr_pos_y, width=1.35 * cm, height=1.35 * cm)

                    elif (df['char_length'][i] > 3.8 and df['char_length'][i] <= 7).any():

                        # Set the font size
                        font_size = 7

                        length = len(value)
                        semi_length = round(length/2)

                        # Draw the label text
                        pdf.setFont("Helvetica", font_size)
                        pdf.drawString(pos_x + 0.07 * cm, pos_y + 1 * cm, value[:semi_length])
                        pdf.setFont("Helvetica", font_size)  # Reduce font size for the second line
                        pdf.drawString(pos_x + 0.07 * cm, pos_y + 0.5 * cm, value[semi_length:])

                        # Draw the QR code
                        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=13.5, border=0 )
                        qr.add_data(value)
                        qr.make(fit=True)
                        qr_img = qr.make_image(fill_color="black", back_color="white")

                        # Calculate the position for drawing the QR code
                        qr_pos_x = pos_x + 1.9 * cm
                        qr_pos_y = pos_y + 0.2 * cm

                        # Draw the QR code
                        qr_img_path = "qr_code.png"
                        qr_img.save(qr_img_path)
                        pdf.drawInlineImage(qr_img_path, qr_pos_x, qr_pos_y, width=1.35 * cm, height=1.35 * cm)

                    elif (df['char_length'][i] > 7 and df['char_length'][i] <= 9.5).any():

                        # Set the font size
                        font_size = 7

                        length = len(value)
                        third_length = round(length/3)

                        # Draw the label text
                        pdf.setFont("Helvetica", font_size)
                        pdf.drawString(pos_x + 0.07 * cm, pos_y + 1.2 * cm, value[:third_length])
                        pdf.setFont("Helvetica", font_size)  # Reduce font size for the second line
                        pdf.drawString(pos_x + 0.07 * cm, pos_y + 0.8 * cm, value[third_length:2*third_length])
                        pdf.setFont("Helvetica", font_size)  # Reduce font size for the second line
                        pdf.drawString(pos_x + 0.07 * cm, pos_y + 0.4 * cm, value[2*third_length:])

                        # Draw the QR code
                        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=13.5, border=0 )
                        qr.add_data(value)
                        qr.make(fit=True)
                        qr_img = qr.make_image(fill_color="black", back_color="white")

                        # Calculate the position for drawing the QR code
                        qr_pos_x = pos_x + 1.9 * cm
                        qr_pos_y = pos_y + 0.2 * cm

                        # Draw the QR code
                        qr_img_path = "qr_code.png"
                        qr_img.save(qr_img_path)
                        pdf.drawInlineImage(qr_img_path, qr_pos_x, qr_pos_y, width=1.35 * cm, height=1.35 * cm)

                    else:

                        # Draw the label text
                        font_size = 7
                        pdf.setFont("Helvetica", font_size)
                        pdf.drawString(pos_x + 0.07 * cm, pos_y + 1.2 * cm, value[:8])
                        pdf.setFont("Helvetica", font_size)  # Reduce font size for the second line
                        pdf.drawString(pos_x + 0.07 * cm, pos_y + 0.8 * cm, value[8:16])
                        pdf.setFont("Helvetica", font_size)  # Reduce font size for the second line
                        pdf.drawString(pos_x + 0.07 * cm, pos_y + 0.4 * cm, value[16:23] + "...")

                        # Draw the QR code
                        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=13.5, border=0 )
                        qr.add_data(value)
                        qr.make(fit=True)
                        qr_img = qr.make_image(fill_color="black", back_color="white")

                        # Calculate the position for drawing the QR code
                        qr_pos_x = pos_x + 1.9 * cm
                        qr_pos_y = pos_y + 0.2 * cm

                        # Draw the QR code
                        qr_img_path = "qr_code.png"
                        qr_img.save(qr_img_path)
                        pdf.drawInlineImage(qr_img_path, qr_pos_x, qr_pos_y, width=1.35 * cm, height=1.35 * cm)


                # Move to the next page
                pdf.showPage()

            # Save and close the PDF file
            pdf.save()
    
        if paramsmall == '1':

            # Splitting the values into groups of 80
            value_groups = [values[i:i + 189] for i in range(0, len(values), 189)]

            # Set up the PDF canvas
            pdf_path = output_folder + "/small_labels_existing.pdf"
            pdf = canvas.Canvas(pdf_path, pagesize=A4)

            # Set the dimensions of the labels in centimeters
            label_width_cm = 2.54 * cm
            label_height_cm = 0.999 * cm

            # Set the spacing between labels
            x_spacing = label_width_cm + 0.25 * cm
            y_spacing = label_height_cm

            # Set the initial position for drawing
            x_start = 0.1  * cm
            y_start = A4[1] - 1.46 * cm

            # Iterate over the value groups
            for group in value_groups:
                # Calculate the number of rows and columns needed for this group
                num_rows = (len(group) - 1) // 7 + 1
                num_cols = min(len(group), 7)

                # Calculate the total width and height needed for this group
                total_width = num_cols * x_spacing
                total_height = num_rows * y_spacing

                # Calculate the starting position for this group
                x = x_start + (A4[0] - total_width) / 2
                y = y_start - total_height

                # Iterate over the values in the group
                for i, value in enumerate(group):
                    # Calculate the position for drawing the value and QR code
                    pos_x = x + (i % 7) * x_spacing
                    pos_y = y + (i // 7) * y_spacing

                    if (df['char_length'][i] <= 1.9).any():

                        # Set the font size
                        font_size = 8

                        # Draw the label text
                        pdf.setFont("Helvetica", font_size)
                        pdf.drawString(pos_x + 0.07 * cm, pos_y + 0.6 * cm, value)

                        # Draw the QR code
                        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=8, border=0 )
                        qr.add_data(value)
                        qr.make(fit=True)
                        qr_img = qr.make_image(fill_color="black", back_color="white")

                        # Calculate the position for drawing the QR code
                        qr_pos_x = pos_x + 1.5 * cm
                        qr_pos_y = pos_y + 0.3 * cm

                        # Draw the QR code
                        qr_img_path = "qr_code.png"
                        qr_img.save(qr_img_path)
                        pdf.drawInlineImage(qr_img_path, qr_pos_x, qr_pos_y, width=0.8 * cm, height=0.8 * cm)

                    elif (df['char_length'][i] > 1.9 and df['char_length'][i] <= 3.6).any():

                        # Set the font size
                        font_size = 8

                        length = len(value)
                        semi_length = round(length/2)

                        # Draw the label text
                        pdf.setFont("Helvetica", font_size)
                        pdf.drawString(pos_x + 0.07 * cm, pos_y + 0.8 * cm, value[:semi_length])
                        pdf.drawString(pos_x + 0.07 * cm, pos_y + 0.45 * cm, value[semi_length:])

                        # Draw the QR code
                        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=8, border=0 )
                        qr.add_data(value)
                        qr.make(fit=True)
                        qr_img = qr.make_image(fill_color="black", back_color="white")

                        # Calculate the position for drawing the QR code
                        qr_pos_x = pos_x + 1.5 * cm
                        qr_pos_y = pos_y + 0.3 * cm

                        # Draw the QR code
                        qr_img_path = "qr_code.png"
                        qr_img.save(qr_img_path)
                        pdf.drawInlineImage(qr_img_path, qr_pos_x, qr_pos_y, width=0.8 * cm, height=0.8 * cm)

                    elif (df['char_length'][i] > 3.6 and df['char_length'][i] <= 7).any():

                        # Set the font size
                        font_size = 8

                        length = len(value)
                        third_length = round(length/3)

                        # Draw the label text
                        pdf.setFont("Helvetica", font_size)
                        pdf.drawString(pos_x + 0.07 * cm, pos_y + 0.85 * cm, value[:third_length])
                        pdf.drawString(pos_x + 0.07 * cm, pos_y + 0.6 * cm, value[third_length:third_length*2])
                        pdf.drawString(pos_x + 0.07 * cm, pos_y + 0.35 * cm, value[third_length*2:])

                        # Draw the QR code
                        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=8, border=0 )
                        qr.add_data(value)
                        qr.make(fit=True)
                        qr_img = qr.make_image(fill_color="black", back_color="white")

                        # Calculate the position for drawing the QR code
                        qr_pos_x = pos_x + 1.5 * cm
                        qr_pos_y = pos_y + 0.3 * cm

                        # Draw the QR code
                        qr_img_path = "qr_code.png"
                        qr_img.save(qr_img_path)
                        pdf.drawInlineImage(qr_img_path, qr_pos_x, qr_pos_y, width=0.8 * cm, height=0.8 * cm)

                    elif (df['char_length'][i] > 7 and df['char_length'][i] <= 9.2).any():

                        # Set the font size
                        font_size = 6

                        length = len(value)
                        third_length = round(length/3)

                        # Draw the label text
                        pdf.setFont("Helvetica", font_size)
                        pdf.drawString(pos_x + 0.06 * cm, pos_y + 0.85 * cm, value[:third_length])
                        pdf.drawString(pos_x + 0.06 * cm, pos_y + 0.6 * cm, value[third_length:third_length*2])
                        pdf.drawString(pos_x + 0.06 * cm, pos_y + 0.35 * cm, value[third_length*2:])

                        # Draw the QR code
                        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=8, border=0 )
                        qr.add_data(value)
                        qr.make(fit=True)
                        qr_img = qr.make_image(fill_color="black", back_color="white")

                        # Calculate the position for drawing the QR code
                        qr_pos_x = pos_x + 1.5 * cm
                        qr_pos_y = pos_y + 0.3 * cm

                        # Draw the QR code
                        qr_img_path = "qr_code.png"
                        qr_img.save(qr_img_path)
                        pdf.drawInlineImage(qr_img_path, qr_pos_x, qr_pos_y, width=0.8 * cm, height=0.8 * cm)

                    else:

                        # Draw the label text
                        font_size = 6
                        pdf.setFont("Helvetica", font_size)
                        pdf.drawString(pos_x + 0.06 * cm, pos_y + 0.85 * cm, value[:7])
                        pdf.drawString(pos_x + 0.06 * cm, pos_y + 0.6 * cm, value[7:14])
                        pdf.drawString(pos_x + 0.06 * cm, pos_y + 0.35 * cm, value[14:20] + "...")

                        # Draw the QR code
                        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=8, border=0 )
                        qr.add_data(value)
                        qr.make(fit=True)
                        qr_img = qr.make_image(fill_color="black", back_color="white")

                        # Calculate the position for drawing the QR code
                        qr_pos_x = pos_x + 1.5 * cm
                        qr_pos_y = pos_y + 0.3 * cm

                        # Draw the QR code
                        qr_img_path = "qr_code.png"
                        qr_img.save(qr_img_path)
                        pdf.drawInlineImage(qr_img_path, qr_pos_x, qr_pos_y, width=0.8 * cm, height=0.8 * cm)

                # Move to the next page
                pdf.showPage()

            # Save and close the PDF file
            pdf.save()

    else:
        print("One or more paramters are empty or not set. Unable to generate pdf. Selected one or more label sizes and enter all needed parameters")

def calculate_text_width(text, font_name, font_size):
    root = tk.Tk()
    test_label = tk.Label(root, text=text, font=(font_name, font_size))
    test_label.pack()
    width_pixels = test_label.winfo_reqwidth()
    root.destroy()

    pixels_per_inch = get_screen_ppi()
    width_cm = width_pixels / (pixels_per_inch * (1 / 2.54))
    return width_cm

def get_screen_resolution():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return screen_width, screen_height

def get_screen_ppi():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    screen_diagonal_pixels = math.sqrt(screen_width**2 + screen_height**2)
    screen_diagonal_inches = math.sqrt((screen_width / root.winfo_fpixels('1i'))**2 + (screen_height / root.winfo_fpixels('1i'))**2)
    ppi = screen_diagonal_pixels / screen_diagonal_inches
    root.destroy()
    return ppi