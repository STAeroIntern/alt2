from library import *
import plot
from openpyxl.styles import Alignment

def run(Data_Lib):
    # Create a new workbook and add a worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Figures"

    # Set up headers
    ws.append(['Date','Time','Description','UAV ID','Remark',"Image"])

    for files in Data_Lib:
        try:
            for Option in ["UAV vs Pri Baro","UAV vs Sec Baro","Pri Baro vs Sec Baro"]:
                #Grab the plot for each files and option and return the figure instead of plotting
                fig,status = plot.run(Data_Lib[files],Option,toggle=0)
                if status == 10: 
                    #Write the image file name
                    fig.write_image(r"D:\alt\save\\"+ str(files) + '_' + Option + '_' + str(Data_Lib[files]['UAV ID'].iloc[0]) + '_' + 'Below Cross-Check Offset' +'.jpg')
                elif status == 11:
                    fig.write_image(r"D:\alt\save\\"+ str(files) + '_' + Option + '_' + str(Data_Lib[files]['UAV ID'].iloc[0]) + '_' + 'Above Cross-Check Offset' +'.jpg')
                elif status == 111:
                    fig.write_image(r"D:\alt\save\\"+ str(files) + '_' + Option + '_' + str(Data_Lib[files]['UAV ID'].iloc[0]) + '_' + 'Cross-Check Fail' +'.jpg')
                else:
                    fig.write_image(r"D:\alt\save\\"+ str(files) + '_' + Option + '_' + str(Data_Lib[files]['UAV ID'].iloc[0]) + '_' + 'Below Offset' +'.jpg')
                
        except:
            continue
    
    # Specify the directory containing the images
    image_directory = r"D:\alt\save\\"
    
    # Iterate through the image directory
    for row_index, img in enumerate(os.listdir(image_directory),start = 2):
        if img.endswith('.jpg'):
        
            # Extract filename without extension
            filename_without_extension = os.path.splitext(os.path.basename(img))[0]
            
            # Split the filename by '_'
            filename_parts = filename_without_extension.split('_')
        
            # Add filename parts into separate columns in the current row
            for col_index, part in enumerate(filename_parts, start=1):
                cell = ws.cell(row=row_index, column=col_index, value=part)
                cell.alignment = Alignment(horizontal='left', vertical='top')  # Top-left alignment


            # Create an image object and specify the full path
            img_path = os.path.join(image_directory, img)
            excel_img = Image(img_path)

            # Insert image in the adjacent cell in column D
            cell_address = f"F{row_index}"  # Adjust for header row
            ws.add_image(excel_img, cell_address)

            # Set row height to accommodate the image
            ws.row_dimensions[row_index].height = excel_img.height


    ws.column_dimensions["A"].width = 15  # Filename
    ws.column_dimensions["B"].width = 15  # Prefix
    ws.column_dimensions["C"].width = 30  # Suffix
    ws.column_dimensions["D"].width = 15  # Suffix
    ws.column_dimensions["E"].width = 15 
    ws.column_dimensions["F"].width = 100  # Image column

    # Save workbook to Excel file
    output_file = r"D:\alt\save\report"+".xlsx"
    wb.save(output_file)

    print("Excel file saved successfully!")

