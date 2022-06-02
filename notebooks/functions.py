# General
import io
import gc
import pandas as pd
import numpy as np
from math import prod



def memory_usage(df):
    """
    Method used to calculate the used of memory based on a specific DataFrame.

    Parameters:
    -----------------
        df (pandas.DataFrame): Dataset to analyze.
        
    Returns:
    -----------------
        memory_usage (string) : The dataset's size on memory.
    """
    
    # Calculating the memory usage based on dataframe.info()
    buf = io.StringIO()
    df.info(buf=buf)
    memory_usage = buf.getvalue().split("\n")[-2]
    
    return (memory_usage)


def df_analysis(df, *args, **kwargs):
    """
    Method used to analyze a DataFrame.

    Parameters:
    -----------------
        df (pandas.DataFrame): Dataset to analyze.

        *args, **kwargs:
        -----------------
            key_columns (list): Dataframe key columns in list format
            analysis_type (str) : Flag to show complete information about the dataset.
                                  The analysis type are:
                                  ["header", "complete"]
                                  "complete" shows all information about the dataset.
                                  By defaut "header".

    Returns:
    -----------------
        None.
        Print the analysis on the Dataset.
    """
    
    if df.empty:
        print("The dataset is empty. Please verify the file.")
    else:
        
        ##################################################
        # Initializing variables
        ##################################################
        
        # Getting the key columns and the analysis type
        key_columns = kwargs.get("key_columns", None)
        analysis_type = kwargs.get("analysis_type", None)
        
        # Defining variables to use
        cols_to_exclude = ["object", "bool", "datetime64", "timedelta", "category"]

        # Calculating total of NaN values
        total_of_NaN = df.isna().sum().sum()

        # Validating whether there is infinite values
        number_of_infinite_values = np.isinf(df.select_dtypes(exclude=cols_to_exclude)).values.sum()

        # Identifying empty columns
        empty_cols = [col for col in df.columns if df[col].isna().all()]

        # Calculating the memory usage based on dataframe.info()
        memory = memory_usage(df)
        
        # Messages for key columns validations
        key_columns_present = "present multiple times in the dataframe."
        key_columns_be_used = "be used as a primary key."
        key_columns_error = "Column does not exist"
        
        ##################################################
        # Printing results
        ##################################################

        print("\nAnalysis header")
        print(80*"-")
        print("- Dataset shape:\t\t\t", df.shape[0], "rows and",
              df.shape[1], "columns")
        
        print("- Total of NaN values:\t\t\t", total_of_NaN)
        print("- Percentage of NaN:\t\t\t",
              round((total_of_NaN/prod(df.shape))
                    * 100, 2), "%") if total_of_NaN > 0 else None
        
        print("- Total of infinite values:\t\t", number_of_infinite_values)
        print("- Percentage of infinite values:\t",
              round((number_of_infinite_values/prod(df.shape))
                    * 100, 2), "%") if number_of_infinite_values > 0 else None
        
        print("- Total of empty columns:\t\t", len(empty_cols))
        
        if df.dropna(axis="rows", how="all").shape[0] < df.shape[0]:
            print("- Total of empty rows:\t\t\t",
                  df.shape[0] - df.dropna(axis="rows", how="all"))
        else:
            print("- Total of empty rows:\t\t\t", "0")
        
        print("- Total of full duplicates rows:\t",
              df[df.duplicated()].shape[0])
        
        print("- Unique indexes:\t\t\t", df.index.is_unique)
        
        print("- Memory usage:\t\t\t\t",
              memory.split("memory usage: ")[1])
        
        if key_columns is not None:

            try:
                if df.size == df.drop_duplicates(key_columns).size:
                    print("\n- The key(s):\t", key_columns, "is not",
                          key_columns_present, "\n\t\t It CAN", key_columns_be_used)
                else:
                    print("\n- The key(s):\t", key_columns, "is", key_columns_present,
                          "\n\t\t It CANNOT", key_columns_be_used)
            except Exception:
                print("\n- The key(s):\t\033[31m", key_columns_error,
                      "\033[0m", sep="")
        
        
        ##################################################
        # To show a detailed analysis
        ##################################################
        if analysis_type == "complete":
            
            # Definning the columns based on whether there is numeric columns
            columns_reduced = [
                "name", "type", "records", "unique"
            ]
            
            columns_complete = columns_reduced + ["# NaN", "% NaN", "mean",
                                                  "min", "25%", "50%",
                                                  "75%", "max", "std"
                                                 ]
            
            # Creating a dataset based on Type object and records by columns
            type_cols = df.dtypes.apply(lambda x: x.name).to_dict()
            df_resume = pd.DataFrame(list(type_cols.items()),
                                     columns=["name", "type"])
            df_resume["records"] = list(df.count())
            df_resume["unique"] = list(df.nunique())
            df_resume["# NaN"] = list(df.isnull().sum())
            df_resume["% NaN"] = list(((df.isnull().sum()
                                        / len(df.index))*100).round(2))
            
            # Adding describing columns
            if (df.select_dtypes(["int64"]).shape[1] > 0 or
                    df.select_dtypes(["float64"]).shape[1] > 0):

                df_desc = pd.DataFrame(df.describe().T).reset_index()
                df_desc = df_desc.rename(columns={"index": "name"})
                df_resume = df_resume.merge(right=df_desc[["name", "mean",
                                                           "min", "25%",
                                                           "50%", "75%",
                                                           "max", "std"]],
                                            on="name", how="left")
                df_resume = df_resume[columns_complete]

            else:
                df_resume = df_resume[columns_reduced]
            
            # Enabling the visualizacion of all columns, rows, cell and floar format
            pd.set_option("display.max_rows", None)  # all rows
            pd.set_option("display.max_columns", None)  # all cols
            pd.set_option("display.max_colwidth", None)  # whole cell
            pd.set_option("display.float_format",
                          lambda x: "%.5f" % x)  # full floating number
            
            print("\n\nDetailed analysis")
            print(80*"-")
            display(df_resume.sort_values("records", ascending=False))
            
            # deleting dataframes and freeing up memory 
            if (df.select_dtypes(["int64"]).shape[1] > 0 or
                    df.select_dtypes(["float64"]).shape[1] > 0):
                del [[df_resume, df_desc]]
            else:
                del [[df_resume]]

            gc.collect()
            df_resume, df_desc = (pd.DataFrame() for i in range(2))
            
            # Disabling the visualizacion of all columns, rows, cell and floar format
            pd.reset_option("display.max_rows")  # reset max of showing rows
            pd.reset_option("display.max_columns")  # reset max of showing cols
            pd.reset_option("display.max_colwidth")  # reset width of showing cols
            pd.reset_option("display.float_format")  # reset float format in cell

        # deleting dataframe and freeing up memory 
        df_resume = pd.DataFrame()
        del df_resume, df
        gc.collect()