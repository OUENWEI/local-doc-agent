import os                                  # Check if the file exists
from langchain_core.tools import tool      # Used for registration tools
from docx import Document                  # Used for handling .docx files
from ..logger import logger            # For generating logs
@tool
def docx_read(filename:str) -> str:
    """
    Read the content of a .docx (Word) file.

    Args:
        filename: Path to the .docx file to read.


    Returns:
        The extracted text content, or a string starting with 'error:' if parsing fails.

    """

    if not os.path.exists(filename):
        logger.info(f"The {filename} file doesn't exist, please check the file path. ")
        return  "error:File not found"
    if  not filename.endswith(".docx"):
        logger.info(f"The {filename} file isn't set up as a docx, the AI seems to have called the wrong tool, please contact the developer.")
        return "error:The file isn't in the specified .docx format"

    try: #Handling damaged documents
        doc = Document(filename)
        para = []
        for p in doc.paragraphs:
            text = p.text.strip()
            if text:#Check if text is not empty
                para.append(text)

        tables_text = [] #Handling tables in documents
        for table in doc.tables:
            for row in table.rows:
                row_text = []
                for cell in row.cells:
                    row_text.append(cell.text.strip())
                tables_text.append(" | ".join(row_text))
        content = "\n".join(para) + "\n" + "\n".join(tables_text)

        if not content.strip(): #Check the document to make sure it's not empty
            return "error:No extractable text found"
        max_chars = 10000
        if len(content) > max_chars:
            temp_path = f"{filename}.full.txt"
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(content)
            return (
                f"warning:Document is too long ({len(content)} chars). "
                f"Full content saved to: {temp_path}\n\n"
                f"Preview:\n\n{content[:max_chars]}"
            )
        return content

    except Exception as e :
        logger.info(f"The {filename} document is corrupted, please check the file.{e} ")
        return f"error:The docx document is corrupted,{str(e)}"
