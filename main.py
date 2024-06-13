import asyncio
from js import document
from pyodide.ffi import create_proxy
from ds_store import DSStore
from io import BytesIO


def reset():
    document.getElementById('error').classList.add('hidden')
    document.getElementById('fileList').innerText = ""


async def process_file(event):
    reset()
    csv_file = document.getElementById('myfile').files.item(0)
    array_buf = await csv_file.arrayBuffer()  # Get arrayBuffer from file
    file_bytes = array_buf.to_bytes()  # convert to raw bytes array
    csv_file = BytesIO(file_bytes)
    try:
        names = extract_names(csv_file)
        print(names)
        document.getElementById(
            'fileList').innerText = "\n".join(names)
    except Exception as e:
        print(e)
        document.getElementById(
            'error').classList.remove('hidden')


def main():
    # Create a Python proxy for the callback function
    # process_file() is your function to process events from FileReader
    file_event = create_proxy(process_file)

    # Set the listener to the callback
    e = document.getElementById("myfile")
    e.addEventListener("change", file_event, False)


def extract_names(file):
    # check if it's a file type python
    d = DSStore.open(file)
    files = set()
    for y in d:
        files.add(y.filename)
    return files


main()
