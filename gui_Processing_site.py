def main():
    import os
    import requests
    import pandas as pd

    username = os.environ.get("username")
    password = os.environ.get("password")
    country = os.environ.get("country")
    site = os.environ.get("site")
    
    # Check if username and password are set (not empty)
    if username and password and country and site:

        # Define the Directus base URL
        base_url = 'http://directus.dbgi.org'

        # Define the login endpoint URL
        login_url = base_url + '/auth/login'
        # Create a session object for making requests
        try:
            session = requests.Session()
            # Send a POST request to the login endpoint
            response = session.post(login_url, json={'email': username, 'password': password})
            if response.status_code == 200:
                data = response.json()['data']
                access_token = data['access_token']
                # Create template dataframe to reserve labels
                raw_data = {'status': 'Active',
                    'country': country,
                    'University_name': site}
        
                template = pd.DataFrame([raw_data for _ in range(1)], columns=['status',
                                            'country',
                                            'University_name'])

                headers = {
                        'Content-Type': 'application/json'
                }
            
                record = template.to_json(orient="records")

                headers = {
                        'Content-Type': 'application/json'
                }

                collection_url = 'http://directus.dbgi.org/items/University'

                #Add the site to the database
                session.headers.update({'Authorization': f'Bearer {access_token}'})
                response = session.post(url=collection_url, headers=headers, data=record)
                if response.status_code == 200:
                    print("Site correctly added")

                elif response.status_code == 400:
                    print("Site already entered")
            else:
                print("Access refused, please check your credentials")
        except:
            print("Make sure you are connected to the UNIFR network")