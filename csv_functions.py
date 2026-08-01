from pandas import read_csv
import os
def Csv_highest(filename:str,parameter:str=None):
    if os.path.exists(f"./files/{filename}"):
        df=read_csv(f"./files/{filename}")
        int_columns = df.select_dtypes(include="int").columns.tolist()
        if parameter == None:
            result=[]
            for int_column in int_columns:
                result.append(f"The data of highest value in column({int_column}) is {df.loc[df[int_column].idxmax()]}")
            return result
        # if parameter == None:
        #     for column in columns:
        #         print(f"The highest value in column({column}) is {df[column].max()}")
        else:
            column=parameter
            return f"The data of highest value in column({column}) is {df.loc[df[column].idxmax()]}"
    else:
        return "file not exists"
def Csv_lowest(filename:str,parameter:str=None):
    if os.path.exists(f"./files/{filename}"):
        df=read_csv(f"./files/{filename}")
        if parameter == None:
            int_columns = df.select_dtypes(include="int").columns.tolist()
            result=[]
            for int_column in int_columns:
                result.append(f"The data of lowest value in column({int_column}) is {df.loc[df[int_column].idxmin()].tolist()}")
            return result
        else:
            column=parameter
            return f"The data of lowest value in column({column}) is {df.loc[df[column].idxmin()].tolist()}"
    else:
        return "file not found"

def Csv_avg(filename:str,parameter:str=None):
    if os.path.exists(f"./files/{filename}"):
        df=read_csv(f"./files/{filename}")
        if parameter == None:
            int_columns = df.select_dtypes(include="int").columns.tolist()
            result=[]
            for int_column in int_columns:
                result.append(f"The mean value in column({int_column}) is {df[int_column].mean()}")
            return result
        else:
            column=parameter
            return f"The mean value in column({column}) is {df[column].mean()}"
    else:
        return "file not found"

def Csv_count(filename:str,parameter:str=None):
    if os.path.exists(f"./files/{filename}"):
        df=read_csv(f"./files/{filename}")
        if parameter == None:
            int_columns = df.select_dtypes(include="int").columns.tolist()
            result=[]
            for int_column in int_columns:
                result.append(f"The number of rows in column({int_column}) is {df[int_column].count()}")
            return result
        else:
            column=parameter
            return f"The number of rows in column({column}) is {df[column].count()}"
    else:
        return "file not found"

def Csv_columns(filename:str):
    df=read_csv(f"./files/{filename}")
    columns=df.columns.tolist()
    return f"columns: {columns}"

def Csv_to_list(filename:str):    
    if os.path.exists(f"./files/{filename}"):
        df=read_csv(f"./files/{filename}")
        data=[]
        for _, row in df.iterrows():
            text = "\n".join(
                f"{column}: {value}"
                for column, value in row.items()
            )
            data.append(text)
        return data
    else:
        return "file not found"
    
def metadata(filename:str):
    if filename != "" and filename.split(".")[-1] == "csv":
        if os.path.exists(f"./files/{filename}") :
            metadata=[]
            metadata.append(Csv_columns(filename))
            metadata.append(Csv_highest(filename))
            metadata.append(Csv_lowest(filename))
            metadata.append(Csv_avg(filename))
            metadata.append(Csv_count(filename))
            return metadata
        else:
            return "no metadata."
    else:
        return "no metadata."

