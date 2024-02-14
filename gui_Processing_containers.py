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
    storage = os.environ.get("storage")
    number_row = os.environ.get("number_rows")
    number_col = os.environ.get("number_cols")
    number = int(os.environ.get("number"))
    output_folder = os.environ.get("output_folder")

    # Check if username and password are set (not empty)
    if username and password and storage and number_row != 0 and number_col != 0 and number != 0 and output_folder:

        #Construct the container prefix with the given dimensions (bigger value first):
        if number_col > number_row:
            container_prefix = "container_" + str(number_col) + "x" + str(number_row) + "_"
        else:
            container_prefix = "container_" + str(number_row) + "x" + str(number_col) + "_"
        
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

        # Update the header to include access token for the request
        session.headers.update({'Authorization': f'Bearer {access_token}'})

        #Extract the last entry in the container_id column for the specific prefix
        container_id = "container_id"
        # Construct the filter as query parameters
        params = {'sort[]': f'-{container_id}'}
        
        collection_url = base_url + '/items/Mobile_Container/' + f'?filter[{container_id}][_starts_with]={container_prefix}&&limit=1' 
        response = session.get(collection_url, params=params)
        data = response.json()
        last_value = data['data'][0][container_id] if data['data'] else "null"
        if last_value != "null":
            last_number = int(last_value.split('_')[2])
        else:
            last_number = 0

        #Define the first number of the list (last number + 1)
        first_number = last_number + 1

        # Create template dataframe to reserve labels
        row_data = {'reserved': 'True',
                    'container_location': storage}
        
        template = pd.DataFrame([row_data for _ in range(number)], columns=['reserved',
                                        'container_location'])

        # Generate the container IDs
        template['container_id'] = [f'{container_prefix}''{:06d}'.format(first_number + i) for i in range(number)]

        # Print the resulting DataFrame
        print(template)

        headers = {
                    'Content-Type': 'application/json'
        }
        
        #Create a list with the asked codes beginning with the first number
        values = [f'{container_prefix}''{:06d}'.format(first_number + i) for i in range(number)]
        
        records = template.to_json(orient="records")

        #Add the codes to the database
        session.headers.update({'Authorization': f'Bearer {access_token}'})
        response = session.post(url=collection_url, headers=headers, data=records)
        print(response.json())

        # Splitting the values into groups of 80 (number of labels per page)
        value_groups = [values[i:i + 80] for i in range(0, len(values), 80)]

        # Set up the PDF canvas
        pdf_path = output_folder + "/container_labels_generated.pdf"
        pdf = canvas.Canvas(pdf_path, pagesize=A4)

        # Set the font size and line height
        font_size = 7.5

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
                pdf.setFont("Helvetica-Bold", font_size)
                pdf.drawString(pos_x + 0.4 * cm, pos_y + 0.9 * cm, value[:10])
                pdf.setFont("Helvetica-Bold", font_size)  # Reduce font size for the second line
                pdf.drawString(pos_x + 0.07 * cm, pos_y + 0.4 * cm, value[10:])

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

    else:
        print("Username and/or password not set. The script will be ignored.")
    # Needs still to add the generated code on directus