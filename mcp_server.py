# mcp_server.py
import os
from mcp.server.fastmcp import FastMCP
from app import analyze_code_with_ai, process_file, process_selected_folders, extract_zip_to_temp, generate_report

app = FastMCP("AI Code Review")

REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

@app.tool()
def review_file(file_path: str) -> str:
    if not os.path.exists(file_path):
        return "⚠️ File not found."
    reviews = process_file(file_path)
    report_filename = f"{os.path.basename(file_path)}_review.docx"
    report_path = os.path.join(REPORTS_DIR, report_filename)
    generate_report(reviews, report_path)
    download_url = f"{app.get_public_url()}/files/{report_filename}"
    return "\n\n".join([f"{f}:\n{r}" for f, r in reviews.items()]) + f"\n\n✅ Download report: {download_url}"

@app.tool()
def review_zip(zip_path: str, folders: list[str] = None) -> str:
    if not os.path.exists(zip_path):
        return "⚠️ ZIP file not found."
    base_path = extract_zip_to_temp(zip_path)
    if not folders:
        folders = [os.path.basename(base_path)]
    reviews = process_selected_folders(base_path, folders)
    if not reviews:
        return "⚠️ No code files found."
    report_filename = f"{os.path.basename(zip_path)}_review.docx"
    report_path = os.path.join(REPORTS_DIR, report_filename)
    generate_report(reviews, report_path)
    download_url = f"{app.get_public_url()}/files/{report_filename}"
    return "\n\n".join([f"{f}:\n{r}" for f, r in reviews.items()]) + f"\n\n✅ Download report: {download_url}"

if __name__ == "__main__":
    app.run()
