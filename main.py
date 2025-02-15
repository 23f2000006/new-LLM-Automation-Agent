from fastapi import FastAPI, HTTPException
from app.task_handler import process_task
from app.file_handler import read_file

app = FastAPI()

@app.post("/run")
async def run_task(task: str):
    try:
        output = process_task(task)
        return {"status": "success", "output": output}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read")
async def read_file_endpoint(path:str):
      return read_file(path)
#     return {"message": "I'm receiving the request"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
