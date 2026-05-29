import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from .schemas import UnitMap
from .generator import generate_unit_map_docx, generate_unit_map_html

app = FastAPI(title="Unit Work Map Generator API")

OUTPUT_DIR = "outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.post("/generate_unit_map")
async def generate_unit_map(unit_map: UnitMap):
    try:
        safe_title = unit_map.title.replace(' ', '_').replace('/', '_').replace('\\', '_')
        docx_filename = f"UnitMap_{safe_title}.docx"
        docx_path = os.path.join(OUTPUT_DIR, docx_filename)
        
        html_filename = f"UnitMap_{safe_title}.html"
        html_path = os.path.join(OUTPUT_DIR, html_filename)
        
        # Use outputs dir for temporary diagrams too
        generate_unit_map_docx(unit_map, docx_path, OUTPUT_DIR)
        generate_unit_map_html(unit_map, html_path)
        
        return {
            "message": "Unit Map generated successfully",
            "docx_url": f"/download/docx/{docx_filename}",
            "html_url": f"/download/html/{html_filename}"
        }
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/docx/{filename}")
async def download_docx(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', filename=filename)
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/download/html/{filename}")
async def download_html(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='text/html', filename=filename)
    raise HTTPException(status_code=404, detail="File not found")

@app.post("/proofread")
async def proofread_text(data: dict):
    text = data.get("text", "")
    if not text:
        return {"corrected_text": ""}
    
    # Simple rule-based proofreading simulation
    # In a real app, this would call an LLM
    lines = text.split("\n")
    corrected_lines = []
    for line in lines:
        line = line.strip()
        if not line: continue
        if not line.startswith("- "):
            line = "- " + line
        if not line.endswith(".") and not line.endswith("함") and not line.endswith("임"):
            line = line + "함."
        corrected_lines.append(line)
    
    return {"corrected_text": "\n".join(corrected_lines)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
