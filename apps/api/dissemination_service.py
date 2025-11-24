from pathlib import Path
import shutil
from fastapi.responses import FileResponse

PUBLIC_DIR = Path("public/reports")

def publish_report(pdf_path: Path, year: int, lang: str):
    # Copie le rapport dans le répertoire public
    target = PUBLIC_DIR / f"{year}_{lang}.pdf"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(pdf_path, target)
    return str(target)

def list_public_reports():
    return [f.name for f in PUBLIC_DIR.glob("*.pdf")]

def get_public_report(filename: str):
    path = PUBLIC_DIR / filename
    if path.exists():
        return FileResponse(str(path), media_type="application/pdf", filename=filename)
    return {"error": "not_found"}
