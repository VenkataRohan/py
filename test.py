import pandas as pd
import requests


excel_file_path = "tst.xlsx"
df = pd.read_excel(excel_file_path)

api_url = "http://localhost:5005"
json_data = requests.get(api_url)


if json_data.status_code == 200:
    # Request was successful
    data = json_data.json()  # Assuming the json_data is in JSON format
else:
    # Request failed
    print("API request failed with status code:", json_data.status_code)



unmatched_list=[]
unmatched_list_domainname_json=[]
unmatched_list_domainname_excel=[]
excel_ids=[]

keys=data[0].keys()
for index, excel_row in df.iterrows():
    # Assuming 'ID' is a unique identifier in your Excel data
    excel_id = excel_row['ID']
    excel_ids.append(excel_id)
    json_entry = next((entry for entry in data if entry.get('ID') == excel_id), None)
     
    unmatched_obj={}
    if json_entry:
        for val in keys:
            if excel_row[val] != json_entry[val]:
                # unmatched_obj[val]={"previous_val":excel_row[val], "updated_val": json_entry[val]}
                unmatched_list.append({"ID":excel_row['ID'],"Column Name":val,"Previous Value":excel_row[val],"Updated Value":json_entry[val]})
                df.at[index,val]=json_entry[val]  
    else:
        unmatched_list_domainname_json.append({"ID":excel_row['ID'],"Domain Name":excel_row['Domain Name']})


#checking missing data in excel 
for entry in data:
    temp=[]
    if  entry.get("ID") not in excel_ids:
        unmatched_list_domainname_excel.append({"ID":entry.get('ID'),"Domain Name":entry.get('Domain Name')})
        for key in keys:
            temp.append(entry.get(key))
        df.loc[len(df.index)] = temp   



# df.loc[len(df.index)] = ['Amy', 89, 93] 

print("Data Frame that is saved in excel")
print(df)


df.to_excel(excel_file_path, index=False)

dataframe_unmatched_col= pd.DataFrame(unmatched_list)
# print()
# print("Data Frame send in email")
# print(dataframe_unmatched_col)


unmatched_list_domainname_excel_df= pd.DataFrame(unmatched_list_domainname_excel)
print()
print("Values present in json missing in excel")
print(unmatched_list_domainname_excel_df)


unmatched_list_domainname_json_df= pd.DataFrame(unmatched_list_domainname_json)
print()
print("Values present in excel missing in json")
print(unmatched_list_domainname_json_df)

