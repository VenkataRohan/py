import pandas as pd
import requests


excel_file_path = "tst2.xlsx"
df = pd.read_excel(excel_file_path)

api_url = "http://localhost:5005"
json_data = requests.get(api_url)

# print(json_data)
if json_data.status_code == 200:
    # Request was successful
    data = json_data.json()  # Assuming the json_data is in JSON format
    # print(data)
else:
    # Request failed
    print("API request failed with status code:", json_data.status_code)



unmatched_list=[]

keys=data[0].keys()
for index, excel_row in df.iterrows():
    # Assuming 'ID' is a unique identifier in your Excel data
    excel_id = excel_row['ID']

    
    
    json_entry = next((entry for entry in data if entry.get('ID') == excel_id), None)
    unmatched_obj={}
    for val in keys:
        if excel_row[val] != json_entry[val]:
            # unmatched_obj[val]={"previous_val":excel_row[val], "updated_val": json_entry[val]}
            unmatched_list.append({"ID":excel_row['ID'],"Column Name":val,"Previous Value":excel_row[val],"Updated Value":json_entry[val]})
            df.at[index,val]=json_entry[val]  

print("Data Frame that is saved in excel")
print(df)


df.to_excel(excel_file_path, index=False)

dataframe_unmatched_col= pd.DataFrame(unmatched_list)
print()
print("Data Frame send in email")
print(dataframe_unmatched_col)

