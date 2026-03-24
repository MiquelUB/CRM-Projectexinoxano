import uvicorn
import os
import sys

# Change to the directory of this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("Starting uvicorn...")
    try:
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
    except Exception as e:
        print(f"Uvicorn crashed with exception: {e}")
        import traceback
        traceback.print_exc()
