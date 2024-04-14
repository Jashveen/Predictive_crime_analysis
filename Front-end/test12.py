# TEAM NAME: Madras Boys
# PROBLEM STATEMENT: Predictive Crime Analytics
# This is the main program that contains every logics and algorithm for spatial analysis
# This code contains: 1.)Authentication for police and users(additional feature).
#                     2.)Logics for 'Spatial analysis' both 'State-wise' and 'District-wise'.




# IMPORTS
from flask import Flask, render_template, request, redirect, session, url_for, flash,send_from_directory,jsonify
import sqlite3
import datetime
import json
import os
import matplotlib
matplotlib.use('Agg') 
import pandas as pd
import folium
import plotly.express as px
from flask import Flask, send_from_directory
import pandas as pd
from geopy.geocoders import ArcGIS
import folium
from folium.plugins import HeatMap
import branca.colormap as cm
import numpy as np
import time


app = Flask(__name__, static_folder=r"C:\Users\Jash Progs\Datathon\Code\Front-end\static")
app.secret_key = 'your_secret_key'

# Function to connect to the SQLite database for police officers.
def get_police_db_connection():
    ''' This function enables connection to store authentication info'''
    conn = sqlite3.connect('police_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to connect to the SQLite database for regular users
def get_user_db_connection():
    ''' This function enables connection to store authentication info'''
    conn = sqlite3.connect('user_database.db')
    conn.row_factory = sqlite3.Row
    return conn

#Function to create an database table and store FIR entries in a database
def create_fir_entry_table():
    conn = get_fir_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS fir_entry (
        district_name TEXT NOT NULL,
        unit_name TEXT NOT NULL,
        fir_no TEXT NOT NULL,
        ri TEXT NOT NULL,
        fir_stage TEXT NOT NULL,
        complaint_mode TEXT NOT NULL,
        crimegroup_name TEXT NOT NULL,
        year_and_month TEXT NOT NULL,
        offence_from_date TEXT NOT NULL,
        offence_to_date TEXT NOT NULL,
        fir_reg_datetime TEXT NOT NULL,
        fir_date TEXT NOT NULL,
        fir_type TEXT NOT NULL,
        crimehead_name TEXT NOT NULL,
        latitude TEXT NOT NULL,
        longitude TEXT NOT NULL,
        actsection TEXT NOT NULL,
        ioname TEXT NOT NULL,
        kgid TEXT NOT NULL,
        ioassigned_date TEXT NOT NULL,
        internal_io TEXT NOT NULL,
        place_of_offence TEXT NOT NULL,
        distance_from_ps TEXT NOT NULL,
        beat_name TEXT NOT NULL,
        village_area_name TEXT NOT NULL,
        male TEXT NOT NULL,
        female TEXT NOT NULL,
        boy TEXT NOT NULL,
        girl TEXT NOT NULL,
        age TEXT NOT NULL,
        victim_count TEXT NOT NULL,
        accused_count TEXT NOT NULL,
        arrested_male TEXT NOT NULL,
        arrested_female TEXT NOT NULL,
        arrested_count TEXT NOT NULL,
        accused_chargesheeted_count TEXT NOT NULL,
        conviction_count TEXT NOT NULL,
        unit_id TEXT NOT NULL,
        crime_no TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

#This route takes care of 'FIR Entry' in the dashboard
@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        # Retrieve form data using snake_case
        district_name = request.form['district_name']
        unit_name = request.form['unit_name']
        fir_no = request.form['fir_no']
        ri = request.form['ri']
        year_and_month = request.form['year_and_month']
        offence_from_date = request.form['offence_from_date']
        offence_to_date = request.form['offence_to_date']
        fir_reg_datetime = request.form['fir_reg_datetime']
        fir_date = request.form['fir_date']
        fir_type = request.form['fir_type']
        fir_stage = request.form['fir_stage']
        complaint_mode = request.form['complaint_mode']
        crimegroup_name = request.form['crimegroup_name']
        crimehead_name = request.form['crimehead_name']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        actsection = request.form['actsection']
        ioname = request.form['ioname']
        kgid = request.form['kgid']
        ioassigned_date = request.form['ioassigned_date']
        internal_io = request.form['internal_io']
        place_of_offence = request.form['place_of_offence']
        distance_from_ps = request.form['distance_from_ps']
        beat_name = request.form['beat_name']
        village_area_name = request.form['village_area_name']
        male = request.form['male']
        female = request.form['female']
        boy = request.form['boy']
        girl = request.form['girl']
        age = request.form['age']
        victim_count = request.form['victim_count']
        accused_count = request.form['accused_count']
        arrested_male = request.form['arrested_male']
        arrested_female = request.form['arrested_female']
        arrested_count = request.form['arrested_count']
        accused_chargesheeted_count = request.form['accused_chargesheeted_count']
        conviction_count = request.form['conviction_count']
        fir_id = request.form['fir_id']
        unit_id = request.form['unit_id']
        crime_no = request.form['crime_no']
        
        # Inserts the form data into the FIR entry database
        conn = get_fir_db_connection()
        conn.execute('''
        
                INSERT INTO fir_entry (
                    district_name,
                    unit_name,
                    fir_no,
                    ri,
                    fir_stage,
                    complaint_mode,
                    crimegroup_name,
                    year_and_month,
                    offence_from_date,
                    offence_to_date,
                    fir_reg_datetime,
                    fir_date,
                    fir_type,
                    crimehead_name,
                    latitude,
                    longitude,
                    actsection,
                    ioname,
                    kgid,
                    ioassigned_date,
                    internal_io,
                    place_of_offence,
                    distance_from_ps,
                    beat_name,
                    village_area_name,
                    male,
                    female,
                    boy,
                    girl,
                    age,
                    victim_count,
                    accused_count,
                    arrested_male,
                    arrested_female,
                    arrested_count,
                    accused_chargesheeted_count,
                    conviction_count,
                    unit_id,
                    crime_no
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                district_name,
                unit_name,
                fir_no,
                ri,
                fir_stage,
                complaint_mode,
                crimegroup_name,
                year_and_month,
                offence_from_date,
                offence_to_date,
                fir_reg_datetime,
                fir_date,
                fir_type,
                crimehead_name,
                latitude,
                longitude,
                actsection,
                ioname,
                kgid,
                ioassigned_date,
                internal_io,
                place_of_offence,
                distance_from_ps,
                beat_name,
                village_area_name,
                male,
                female,
                boy,
                girl,
                age,
                victim_count,
                accused_count,
                arrested_male,
                arrested_female,
                arrested_count,
                accused_chargesheeted_count,
                conviction_count,
                unit_id,
                crime_no
            ))

        conn.commit()
        conn.close()

        flash('FIR entry submitted successfully!', 'success')
        return redirect('/')
    elif request.method == 'GET':
        if 'username' in session:
            current_year_and_month = datetime.datetime.now().strftime("%Y-%m")
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return render_template('submit_form.html', current_year_and_month=current_year_and_month, current_datetime=current_datetime)
        else:
            return redirect(url_for('authentication'))
    else:
        flash('Invalid request method.', 'error')
        return redirect('/')
    
#This function is to ensure that a new table is not created upon authentication
# Function to create the police users table if it does not exist
def create_police_users_table():
    print("Creating police_users table...")
    conn = get_police_db_connection()
    
    # Drop the existing police_users table if it exists
    conn.execute('DROP TABLE IF EXISTS police_users')
    
    # Create a new police_users table with the correct structure
    conn.execute('''
        CREATE TABLE IF NOT EXISTS police_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("police_users table created.")
    

# Function to create a new police user
def create_police_user(username, password):
    conn = get_police_db_connection()
    conn.execute('INSERT INTO police_users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()


# Function to validate credentials for police users
def validate_police_credentials(username, password):
    conn = get_police_db_connection()
    user = conn.execute('SELECT * FROM police_users WHERE username = ? AND password = ?', (username, password)).fetchone()
    if conn:
        conn.close()
    return user is not None


# Route for the signup page for police users
@app.route('/signup_police', methods=['GET', 'POST'])
def signup_police():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Please provide both username and password.', 'error')
        elif user_exists(username, 'police'):
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            create_police_user(username, password)
            flash('Sign up successful! Please login.', 'success')
            return redirect(url_for('login_police'))  # Redirect to the police login page after successful signup

    return render_template('signup_police.html')


# Function to check if a user exists in the database
def user_exists(username, user_type):
    conn = None
    if user_type == 'police':
        conn = get_police_db_connection()
        user = conn.execute('SELECT * FROM police_users WHERE username = ?', (username,)).fetchone()
    if conn:
        conn.close()  # Close the connection
    return user is not None


# Route for the police login page
@app.route('/login_police', methods=['GET', 'POST'])
def login_police():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Please provide both username and password.', 'error')
        elif not validate_police_credentials(username, password):
            flash('Invalid username or password. Please try again.', 'error')
        else:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('police_dashboard'))  # Redirect to the police dashboard after successful login

    return render_template('login_police.html')



# Function to create the regular users table if it does not exist
def create_user_users_table():
    conn = get_user_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Route for the authentication page
@app.route('/')
@app.route('/authentication')
def authentication():
    return render_template('authentication.html')


# Route for the signup page for regular users
@app.route('/signup_user', methods=['GET', 'POST'])
def signup_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Please provide both username and password.', 'error')
        elif user_exists(username, 'user'):
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            conn = get_user_db_connection()
            conn.execute('INSERT INTO user_users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            flash('Sign up successful! Please login.', 'success')
            return redirect(url_for('login_user'))  # Redirect to the regular user login page after successful signup

    return render_template('signup_user.html')

# Function to validate credentials for regular users
def validate_user_credentials(username, password):
    conn = get_user_db_connection()
    user = conn.execute('SELECT * FROM user_users WHERE username = ? AND password = ?', (username, password)).fetchone()
    if conn:
        conn.close()
    return user is not None

# Route for the regular user login page
@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Please provide both username and password.', 'error')
        elif not validate_user_credentials(username, password):
            flash('Invalid username or password. Please try again.', 'error')
        else:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('user_home'))  # Redirect to the user home page after successful login

    return render_template('login_user.html')

# Route for the logout functionality
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('authentication'))  # Redirect to the authentication page after logout

# Route for the user home page
@app.route('/user_home')

def user_home():
    if 'username' in session:
        return render_template('user_home.html', username=session['username'])
    
    return redirect(url_for('authentication'))

# Route for the police dashboard
@app.route('/police_dashboard')
def police_dashboard():
    if 'username' in session:
        return render_template('police_dashboard.html', username=session['username'])
    return redirect(url_for('authentication'))

import sqlite3


# FUNCTION TO SEARCH THROUGH FIR RECORD IN OUR DATABASE
def get_column_names(table_name):
    conn = sqlite3.connect(r"C:\Users\Jash Progs\Datathon\Code\existing_database.db")
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    conn.close()
    return [column[1] for column in columns]

def find_fir_entries(search_criteria):
    # Connect to the database
    conn = sqlite3.connect(r"C:\Users\Jash Progs\Datathon\Code\existing_database.db")
    cursor = conn.cursor()

    # Fetch all data from the table
    cursor.execute("SELECT * FROM fir_entry")
    all_entries = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Filter entries based on search criteria
    filtered_entries = []
    for entry in all_entries:
        if matches_search_criteria(entry, search_criteria):
            filtered_entries.append(entry)

    return filtered_entries

def matches_search_criteria(entry, search_criteria):
    # Define the columns to match
    columns_to_match = ['district_name', 'village_area_name', 'beat_name', 
                        'fir_id', 'unit_id', 'firno', 'unitname']
    
    # Convert the entry tuple to a dictionary with column names as keys
    entry_dict = {column.lower(): value.lower() for column, value in zip(search_criteria.keys(), entry)}

    # Check if any of the specified columns in the entry match the corresponding search criteria
    for column, value in search_criteria.items():
        if column.lower() in entry_dict and value.lower() in entry_dict[column.lower()]:
            return True
    return False

# ROUTE TO SEARCH THROUGH DATABASE 
@app.route('/search_database', methods=['GET', 'POST'])
def search_database():
    if 'username' not in session:
        return redirect(url_for('authentication'))
   
    if request.method == 'POST':
        # Get column names dynamically
        table_name = "fir_entry"  # Change this to your table name
        column_names = get_column_names(table_name)
        
        # Retrieve form data and create search_criteria dictionary
        search_criteria = {
            key.lower(): request.form.get(key, '') for key in column_names
        }

        # Call function to find FIR entries based on search criteria
        search_results = find_fir_entries(search_criteria)

        # Pass search results to search_result.html template
        return render_template('search_result.html', search_results=search_results)

    return render_template('search_database.html')

# THIS ROUTE HANDLES EVERY LOGIC AND ALGORITHMS FOR 'SPATIAL ANALYSIS'

# Route for crime analysis
@app.route('/crime_analysis')
def crime_analysis():
    return render_template('spatial_analysis4.html')

# Route for performing analysis
@app.route('/perform_analysis')
def analyze_data():  
    ''' THIS FUNCTION COUNTS NO OF CRIMES OVER DIFFERENT DISTRICTS AND PRODUCES GRAPHS AUTOMATICALLY'''
    option = request.args.get('option')

    if option == "location":
        # ReadS our CSV dataset
        df = pd.read_csv(r"C:\Users\Jash Progs\Datathon\dataset\officialdataset\pcadata\FIR_Details_Data.csv")

        # Groups by 'District_Name' and count the number of entries per district
        district_counts = df['District_Name'].value_counts().reset_index()
        district_counts.columns = ['District_Name', 'Entry_Count']

        # Plots bar chart using Plotly
        fig_bar = px.bar(district_counts, x='District_Name', y='Entry_Count', title='Number of Entries per District')
        bar_chart_path = os.path.join(app.root_path, 'static', 'bar_chart_districts.html')
        fig_bar.write_html(bar_chart_path)

        # Plots pie chart using Plotly
        fig_pie = px.pie(district_counts, values='Entry_Count', names='District_Name', title='Distribution of Entries by District')
        pie_chart_path = os.path.join(app.root_path, 'static', 'pie_chart_districts.html')
        fig_pie.write_html(pie_chart_path)

# Route for generating choropleth map
@app.route('/choropleth_map')
def generate_choropleth_map():
    '''THIS FUNCTION CREATES AN HEATMAP BASED ON COUNT OF CRIMES DISTRICT-WISE'''
    # Loads the CSV dataset
    csv_data = pd.read_csv(r"C:\Users\Jash Progs\Datathon\dataset\officialdataset\pcadata\FIR_Details_Data.csv")

    # Creates a dictionary to map district names from the CSV to the GeoJSON file
    district_mapping = {
        'Ballari': 'Bellary',
        'Bagalkot':'Bagalkot',
        'Bidar':'Bidar',
        'Koppal':'Koppal',
        'Gadag':'Gadag',
        'Haveri':'Haveri',
        'Uttara Kannada':'Uttar Kannand',
        'Belagavi City': 'Belgaum',
        'Belagavi Dist': 'Belgaum',
        'Davanagere':'Davanagere',
        'Bengaluru City': 'Bangalore Rural',
        'Bengaluru Dist': 'Bangalore Urban',
        'Chamarajanagar': 'Chamrajnagar',
        'Chitradurga':'Chitradurga',
        'Chickballapura': 'Kolar',  # This district is not present in the GeoJSON file, so we'll map it to Kolar
        'Coastal Security Police': None,  # This is not a district, so we'll ignore it
        'Dakshina Kannada': 'Dakshin Kannad',
        'Chikkamagaluru':'Chikmagalur',
        'Hassan':'Hassan',
        'Kodagu':'Kodagu',
        'Mandya':'Mandya',
        'Hubballi Dharwad City': 'Dharwad',
        'ISD Bengaluru': None,  # This is not a district, so we'll ignore it
        'K.G.F': 'Kolar',  # This district is not present in the GeoJSON file, so we'll map it to Kolar
        'Kalaburagi': 'Gulbarga',
        'Kalaburagi City': 'Gulbarga',
        'Karnataka Railways': None,  # This is not a district, so we'll ignore it
        'Mangaluru City': 'Dakshin Kannad',
        'Mysuru City': 'Mysore',
        'Mysuru Dist': 'Mysore',
        'Ramanagara': 'Bangalore Rural',  # This district is not present in the GeoJSON file, so we'll map it to Bangalore Rural
        'Shivamogga': 'Shimoga',
        'Tumakuru': 'Tumkur',
        'Vijayanagara': 'Bellary',
        'Vijayapur': 'Bijapur',
        'Yadgir': 'Raichur'  # This district is not present in the GeoJSON file, so we'll map it to Raichur
     }

    # Maps the district names in the CSV to the GeoJSON file
    csv_data['District_Name'] = csv_data['District_Name'].map(district_mapping)

    # Drops rows with None values in the 'District_Name' column
    csv_data.dropna(subset=['District_Name'], inplace=True)

    # Counts the number of entries district-wise
    district_counts = csv_data['District_Name'].value_counts().reset_index()
    district_counts.columns = ['District_Name', 'Count']

    # Converts the district_counts DataFrame to a dictionary
    district_counts_dict = dict(zip(district_counts['District_Name'], district_counts['Count']))

    # Loads the Karnataka GeoJSON file
    with open(r"C:\Users\Jash\karnataka.geojson", 'r') as f:
        karnataka_districts = json.load(f)

    # Merges the counts with the GeoJSON file
    for feature in karnataka_districts['features']:
        district_name = feature['properties']['NAME_2']
        count = district_counts_dict.get(district_name, 0)
        feature['properties']['Count'] = count

    # Creates a new dataframe with required columns
    df = pd.DataFrame([feature['properties'] for feature in karnataka_districts['features']])

    # Calculates the mean value of 'Count'
    mean_value = csv_data['District_Name'].value_counts().mean()

    # Defines a function to map counts to risk levels based on the mean value
    def map_count_to_risk(count):
        if count < mean_value * 0.5:
            return 'Safe'
        elif count < mean_value * 1.5:
            return 'Risk'
        else:
            return 'High Risk'

    # Creates a new column in the dataframe that maps counts to risk levels
    df['Risk Level'] = df['Count'].apply(map_count_to_risk)

    # Defines the color scale
    color_scale = ['green','yellow', 'red']

    # Creates the choropleth map
    fig = px.choropleth(
        df,
        geojson=karnataka_districts,
        locations='NAME_2',
        featureidkey='properties.NAME_2',
        color='Risk Level',
        color_discrete_sequence=color_scale,  # Use the discrete color scale
        title='FIR Entries in Karnataka Districts',
        hover_name='NAME_2',
        hover_data={'Count': True}
    )

    # Updates the color bar
    fig.update_layout(
        coloraxis_colorbar=dict(
            title='Risk Level',
            tickvals=[0, 1, 2],  # Set the tick values to match the color scale
            ticktext=['low', 'high', 'extreme']  # Set the tick labels to the desired text
        )
    )

    # Updates the hover template
    fig.update_traces(hovertemplate='District_Name: %{hovertext}<br>Count: %{customdata[0]}')


    fig.update_geos(fitbounds="locations", visible=False)

    # Save the figure as an HTML file
    choropleth_map_path = os.path.join(app.root_path, 'static', 'choropleth_map.html')
    fig.write_html(choropleth_map_path)


@app.route('/generate_heatmap/<district>')
def generate_heatmap(district):
     
     print("District:", district)  # This line to check if the district is received correctly

     if district:
        # Loads the CSV dataset
        data = pd.read_csv(r"C:\Users\Jash Progs\Datathon\dataset\officialdataset\pcadata\FIR_Details_Data.csv",low_memory=False)

        # Filters the data for the specified district
        district_data = data[data['District_Name'] == district]

        # Gets the most common crime and most cases month
        most_common_crime = district_data['CrimeGroup_Name'].value_counts().index[0]
        most_cases_month = district_data['Month'].value_counts().index[0]
        print("Most common crime:", most_common_crime)
        print("Most cases month:", most_cases_month)

        # Gets the beat with the highest and lowest crime counts
        beat_counts = district_data['Beat_Name'].value_counts()
        highest_beat = beat_counts.index[0]
        lowest_beat = beat_counts.index[-1]
        print("Highest crime beat:", highest_beat)
        print("Lowest crime beat:", lowest_beat)

        # Gets the unique village names
        villages = district_data['Village_Area_Name'].unique()

        # Function to geocode a village
        def geocode_village(village):
            try:
                location = geolocator.geocode(f"{village}, {district}, Karnataka, India")
                return (location.latitude, location.longitude)
            except:
                return None

        # Initialize the geolocator
        geolocator = ArcGIS()

        # Gets the coordinates for each village
        coordinates = []
        for village in villages:
            coordinates.append(geocode_village(village))
            time.sleep(1)  # Add a 1-second delay between requests

        # Creates a dictionary to store the crime counts for each village
        crime_counts = {}

        # Iterates through the dataset and update the crime counts for each village
        for index, row in district_data.iterrows():
            village = row['Village_Area_Name']
            if village in crime_counts:
                crime_counts[village] += 1
            else:
                crime_counts[village] = 1

        # Creates a list of tuples containing the village name, latitude, longitude, and crime count
        village_data = []
        for village, count in crime_counts.items():
            location = geocode_village(village)
            if location is not None:
                village_data.append((village, location[0], location[1], count))

        # Uses the folium library to create a map and plot the crime counts using markers with different colors based on the crime count
        map_district = folium.Map(location=[16.1875, 75.7170], zoom_start=10)

        # Creates a list of colors based on the crime count
        crime_counts_array = np.array(list(crime_counts.values()))
        normalized_crime_counts = (crime_counts_array - crime_counts_array.min()) / (crime_counts_array.max() - crime_counts_array.min())
        colors = [cm.LinearColormap(['green', 'orange', 'red'])(x) for x in normalized_crime_counts]

        # Adds a heatmap to the map using the village data
        HeatMap(
            [[row[1], row[2], row[3]] for row in village_data],
            min_opacity=0.2,
            max_val=max(count for _, _, _, count in village_data),
            radius=15,
            blur=15,
            max_zoom=1,
            colormap=colors,
        ).add_to(map_district)

        # Saves the map as an HTML file
        map_filename = f"{district}_crime_map.html"
        map_district.save(map_filename)

        return jsonify({
            'heatmap_filename': map_filename,
            'printed_statements': [
                f'District: {district}',
                f'Most common crime: {most_common_crime}',
                f'Most cases month: {most_cases_month}',
                f'Highest crime beat: {highest_beat}',
                f'Lowest crime beat: {lowest_beat}',
            ],
        });

     else:
        return 'No district selected', 400

# Route for serving bar chart HTML file
@app.route('/bar_chart')
def serve_bar_chart():
    return send_from_directory('static', 'bar_chart_districts.html')

# Route for serving pie chart HTML file
@app.route('/pie_chart')
def serve_pie_chart():
    return send_from_directory('static', 'pie_chart_districts.html')

@app.route('/choropleth_map_html')
def serve_choropleth_map_html():
    choropleth_map_path = os.path.join(app.root_path, 'static', 'choropleth_map.html')
    with open(choropleth_map_path, 'rb') as f:
        html_content = f.read()
        # print(html_content)  # Uncomment this line if you want to print the file contents
    return html_content, 200, {'Content-Type': 'text/html'}
        
# Function to connect to the SQLite database for FIR entries
def get_fir_db_connection():
    conn = sqlite3.connect('fir_entry.db')  
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == '__main__':
    create_user_users_table()
    create_fir_entry_table()
    app.run(debug=True)
