from library import *
import func
import read
import split
import export
import plot

#Webpage Customization
st.set_page_config(layout="wide")

#Path
#source = r"C:\Users\AIRSHOW\Downloads\Raw To Engineering Logs Converter\Engineering Logs\\"
#destination = r"D:\alt\split\\"
@st.cache_data
def process_zip(uploaded_file):
    # Dictionary to store DataFrames with filename as the key
    file_dataframes = {}
    # Dictionary to store file sizes (in bytes) with filename as the key
    file_sizes = {}

    # Use zipfile to open the ZIP archive
    with zipfile.ZipFile(io.BytesIO(uploaded_file.read())) as zf:
        # List the files inside the ZIP archive
        file_names = zf.namelist()
        
        # Loop through the files and read them as CSVs
        for file_name in file_names:
            if file_name.endswith('.txt'):  # Assuming the text files are CSV-formatted
                with zf.open(file_name) as file:
                    try:
                        # Read the content of the text file as a DataFrame
                        df = pd.read_csv(file)
                        
                        # Get the file size in bytes
                        file_size = zf.getinfo(file_name).file_size
                        
                        # Store the DataFrame and file size in respective dictionaries
                        file_dataframes[file_name] = df
                        file_sizes[file_name] = file_size  # File size in bytes
                    except Exception as e:
                        st.write(f"Error reading {file_name}: {e}")

    return file_dataframes, file_sizes


#Function to read raw files
#@st.cache_data

def run(file_dataframes, file_sizes):
        
        # Step 3: Apply the first filter to the extracted data
        data_lib = read.run(file_dataframes, file_sizes,func.filter1)
    
        # Step 4: Create a ZIP file for download containing the filtered data
        #Split the telemetry files if there are double sorties in one files.
        zip_buffer = split.run(data_lib)

        st.download_button(
        label="Download All CSVs as ZIP",
        data=zip_buffer,
        file_name="split_csvs.zip",
        mime="application/zip"
        )
        
        # Step 5: Upload the processed ZIP file for further filtering (second filter)
        st.subheader("Upload the Processed ZIP(Split CSV files)")
        processed_zip_file = st.file_uploader("Upload processed ZIP file", type="zip")

        if processed_zip_file is not None:
            # Step 6: Process the uploaded processed ZIP file to extract data
            second_filtered_data, second_file_sizes = process_zip(processed_zip_file)

        #Run the third filter
        data_lib3 = read.run(second_filtered_data, second_file_sizes,func.filter2)

        return data_lib3 


# def run(source, destination):

#     #Run the first filter 
#     data_lib = read.run(source,func.filter1)
    
#     #Split the telemetry files if there are double sorties in one files.
#     parent_path2 = split.run(data_lib,destination)

#     #Run the third filter
#     data_lib3 = read.run(parent_path2,func.filter2)

#     return data_lib3

# final_data = run(source,destination)

# Step 1: Upload the ZIP file of unprocessed data
uploaded_file = st.file_uploader("Upload a ZIP file containing text (CSV) files", type="zip")

# If a file is uploaded
if uploaded_file is not None:
    # Step 2: Process the uploaded ZIP to extract data and file sizes
    file_dataframes, file_sizes = process_zip(uploaded_file)
    final_data = run(file_dataframes, file_sizes)

    #Streamlit web section
    files = list(final_data.keys())
    telemetry_file = st.selectbox("Select files to view", files)

    tabs1, tabs2 = st.tabs(['Telemetry', 'Plot'])

    with tabs1:
        #Print out the dataframe of the telemetry they want to view
        st.dataframe(final_data[telemetry_file])

    with tabs2:
        #User will select the graph they want to plot
        selection = st.selectbox("Select Plot", ['UAV vs Pri Baro', 'UAV vs Sec Baro', 'Pri Baro vs Sec Baro'])

        #After selection (plot the relevant graph selected)
        plot.run(final_data[telemetry_file],selection,toggle=1)

        # Button to generate altitude report
        generate = st.button('Generate Report')

        #Function to generate if the button is pressed
        if generate:
            with st.spinner('Wait for it...'):
                #Generate report
                export.run(final_data)
                st.success("Report Generated")

else:
    st.write("File Upload Error")











