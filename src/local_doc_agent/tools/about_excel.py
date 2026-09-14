import os
import pandas as pd
from langchain_core.tools import tool
from local_doc_agent.logger import logger

MAX_chars = 10000


@tool
def excel_read(filename: str) -> str :
    """Read the content of an Excel file (.xlsx).

        Use this tool when the user wants to read, summarize, extract, or analyze
        an Excel spreadsheet. Returns the first sheet as CSV-formatted text.

        Args:
            filename: Absolute or relative path to the .xlsx file.

        Returns:
            A string containing the CSV-formatted content of the first sheet.
            On failure, returns a string starting with 'error:' such as
            'error:File not found' or 'error:The file isn't in the specified .xlsx format'.
    """


    if not os.path.exists(filename): #Check if the file exists
        logger.info(f"The excel {filename} does not exist")
        return "error:File not found"
    if not filename.endswith(".xlsx") :#Check if the file is a non-.xlsx worksheet
        logger.info(f"The excel {filename} is not an Excel file")
        return "error:The file isn't in the specified .xlsx format"
    try :#Prevent input from being corrupted files
        dv = pd.read_excel(filename)
    except Exception as e:
        logger.info(f"Failed to parse '{filename}': {e}")
        return "error:Failed to parse the file. It may be corrupted or password-protected."


    rows,cols = dv.shape
    if rows == 0:
        logger.info(f"The excel {filename} is empty")
        return "error:No extractable data found in the file"

    content = dv.to_csv(index=False)
    if len(content) > MAX_chars:  #Check the file length
        logger.warning(
            f"File too large: {filename}, "
            f"chars={len(content)}, rows={rows}, cols={cols}"
        )
        return (
            f"error:File is too large ({len(content)} chars, {rows} rows, {cols} cols). "
            f"Large file support (RAG) will be added in a future version. "
            f"Please reduce the file size or split it into smaller files."
        )

    logger.info(f"Successfully read Excel file: {filename}, {rows} rows")
    return content






