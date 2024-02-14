def main():

    import requests
    import os
    import pandas as pd
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    import qrcode

    #Variables of the first window (generate from scratch)
    username = os.environ.get("username")
    password = os.environ.get("password")
    location = os.environ.get("location")
    storage = os.environ.get("storage")
    number = int(os.environ.get("number"))
    output_folder = os.environ.get("output_folder")

    # Check if username and password are set (not empty)
    if username and password and location and storage and number != 0 and output_folder:
        parambig1 = os.environ.get("parambig1")
        paramsmall11 = os.environ.get("paramsmall11")
        paramsmall21 = os.environ.get("paramsmall21")

        # Define the Directus base URL
        base_url = 'http://directus.dbgi.org'

        # Define the login endpoint URL
        login_url = base_url + '/auth/login'
        # Create a session object for making requests
        session = requests.Session()
        # Send a POST request to the login endpoint
        response = session.post(login_url, json={'email': username, 'password': password})
        data = response.json()['data']
        access_token = data['access_token']

        #Extract the last entry in the DBGI_SPL_ID column of the samples collection
        DBGI_SPL_ID = 'DBGI_SPL_ID'
        params = {'sort[]': f'-{DBGI_SPL_ID}'}
        collection_url = base_url + '/items/samples'
        response = session.get(collection_url, params=params)
        last_value = response.json()['data'][0][DBGI_SPL_ID]
        last_number = int(last_value.split('_')[1])

        # Create template dataframe to reserve labels
        row_data = {'Reserved': 'True',
                    'BG': location,
                    'sample_location': storage}
        
        template = pd.DataFrame([row_data for _ in range(number)], columns=['Reserved',
                                        'BG',
                                        'sample_location'])

        headers = {
                    'Content-Type': 'application/json'
        }
        
        #Define the first number of the list (last number + 1)
        first_number = last_number + 1
        
        #Create a list with the asked codes beginning with the first number
        values = ['dbgi_{:06d}'.format(first_number + i) for i in range(number)]
        
        records = template.to_json(orient="records")
        print(records)

        #Add the codes to the database
        session.headers.update({'Authorization': f'Bearer {access_token}'})
        response = session.post(url=collection_url, headers=headers, data=records)
        print(response.json())

        #Check if big labels are asked to generate the pdf
        if parambig1 == '1':

            # Splitting the values into groups of 80 (number of labels per page)
            value_groups = [values[i:i + 80] for i in range(0, len(values), 80)]

            # Set up the PDF canvas
            pdf_path = output_folder + "/big_labels_generated.pdf"
            pdf = canvas.Canvas(pdf_path, pagesize=A4)

            # Set the font size and line height
            font_size = 12

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

                    # Draw the label text
                    pdf.setFont("Helvetica", font_size)
                    pdf.drawString(pos_x + 0.55 * cm, pos_y + 0.9 * cm, value[:5])
                    pdf.setFont("Helvetica", font_size)  # Reduce font size for the second line
                    pdf.drawString(pos_x + 0.3 * cm, pos_y + 0.4 * cm, value[5:])

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

        #Check if extraction labels are asked to generate the pdf
        if paramsmall11 == '1':

            #Add the extraction suffix
            values = [item + '_01' for item in values]

            # Splitting the values into groups of 80
            value_groups = [values[i:i + 189] for i in range(0, len(values), 189)]

            # Set up the PDF canvas
            pdf_path = output_folder + "/extraction_labels_generated.pdf"
            pdf = canvas.Canvas(pdf_path, pagesize=A4)

            # Set the font size and line height
            font_size = 8

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

                    # Draw the label text
                    pdf.setFont("Helvetica", font_size)
                    pdf.drawString(pos_x + 0.5 * cm, pos_y + 0.9 * cm, value[:5])
                    #pdf.setFont("Helvetica", font_size)  # Reduce font size for the second line
                    pdf.drawString(pos_x + 0.3 * cm, pos_y + 0.55 * cm, value[5:11])
                    pdf.drawString(pos_x + 0.5 * cm, pos_y + 0.25 * cm, value[11:])

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
        
        #Check if injection labels are asked to generate the pdf
        if paramsmall21 == '1':

            #Add the injection suffix
            values = [item + '_01' for item in values]

            # Splitting the values into groups of 80
            value_groups = [values[i:i + 189] for i in range(0, len(values), 189)]

            # Set up the PDF canvas
            pdf_path = output_folder + "/injection_labels_generated.pdf"
            pdf = canvas.Canvas(pdf_path, pagesize=A4)

            # Set the font size and line height
            font_size = 8

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

                    # Draw the label text
                    pdf.setFont("Helvetica", font_size)
                    pdf.drawString(pos_x + 0.5 * cm, pos_y + 0.9 * cm, value[:5])
                    #pdf.setFont("Helvetica", font_size)  # Reduce font size for the second line
                    pdf.drawString(pos_x + 0.3 * cm, pos_y + 0.55 * cm, value[5:11])
                    pdf.drawString(pos_x + 0.3 * cm, pos_y + 0.25 * cm, value[11:])

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
        print("Username and/or password not set. The script will be ignored.")
    # Needs still to add the generated code on directus