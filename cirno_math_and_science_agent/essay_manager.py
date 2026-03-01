from cirno_math_and_science_agent.config import settings
import logging
import fitz
import re

logger = logging.getLogger("essay_manager")
# Load PDF
def load_pdf(path: str):
    # load pdf through fitz
    logger.info(f"Loading PDF: {path}")
    loader = fitz.open(path)
    pages = []
    for page in loader:
        pages.append(page.get_text())
    loader.close()
    return pages
# Get work id
def get_work_id(url: str):
    match = re.search(r"https://openalex\.org/(W\d+)", url)
    if match:
        work_id = match.group(1)
        return work_id