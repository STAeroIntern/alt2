from library import *
import func

def run(data_lib, sizes, _filter_func):
    # Create an empty library to store the filtered data and file size
    filtered_data_lib = {}
    filtered_sizes = {}

    # Size limits
    min_size = 321410  # Minimum file size in bytes
    max_size = 400845463  # Maximum file size in bytes

    # Iterate over the data (already loaded from process_zip)
    for file_name, data in data_lib.items():
        file_size = sizes.get(file_name)

        # Skip files that are above or below the specified size limits
        if file_size is None or file_size >= max_size or file_size <= min_size:
            continue  # Skip this file if it's outside the size range

        try:
            # Apply the filter function to the DataFrame
            filtered_data = _filter_func(data)
            if isinstance(filtered_data, pd.DataFrame):
                filtered_data_lib[file_name] = filtered_data
                filtered_sizes[file_name] = file_size  # Store the file size in the dictionary
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
            continue

    # Remove smaller files with similar names (if required)
    keys = list(filtered_sizes.keys())
    keys_to_remove = []

    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            filename1, filename2 = keys[i], keys[j]
            if func.compare(filename1, filename2):
                # Compare file sizes and add the smaller one to the removal list
                keys_to_remove.append(filename1 if filtered_sizes[filename1] < filtered_sizes[filename2] else filename2)
                break

    # Remove the files marked for deletion
    for key in keys_to_remove:
        filtered_data_lib.pop(key, None)
        filtered_sizes.pop(key, None)

    return filtered_data_lib


# def run(parent_path, _filter_func):
#     #Create two empty library to store the data and file size
#     data_lib = {}
#     sizes = {}

#     for file in os.listdir(parent_path):
#         file_path = os.path.join(parent_path, file)
#         files_size = os.path.getsize(file_path)
#         #Remove files that are above or equal to this byte size
#         if ((files_size >= 400845463) | (files_size <= 321410)): 
#             os.remove(file_path)

#         trim_name = file[0:15]
#         #pool = Pool(8) #
#         try:
#             #data = pool.map(func.reader, file_path)
#             data = pd.read_csv(file_path)
#             filtered_data = _filter_func(data)  # Call the filter function
#             if isinstance(filtered_data, pd.DataFrame):
#                 data_lib[trim_name] = filtered_data
#                 sizes[trim_name] = os.path.getsize(file_path)
#         except Exception as e:
#             print(f"Error reading {file}: {e}")
#             continue

#     # Remove smaller files with similar names
#     keys = list(sizes.keys())
#     keys_to_remove = []

#     for i in range(len(keys)):
#         for j in range(i + 1, len(keys)):
#             filename1, filename2 = keys[i], keys[j]
#             if func.compare(filename1, filename2):
#                 # Compare file sizes and add the smaller one to removal list
#                 keys_to_remove.append(filename1 if sizes[filename1] < sizes[filename2] else filename2)
#                 break

#     for key in keys_to_remove:
#         data_lib.pop(key, None)
#         sizes.pop(key, None)  

#     return data_lib