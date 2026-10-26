from pathlib import Path
import re

LANGUAGES: list[str] = ["Python", "Java", "TypeScript", "JavaScript", "HTML", "CSS", "SQL", "C#"]
FRAMEWORKS: list[str] = ["Node.js", "LangChain", "LangGraph", "AutoGen", "AWS", "Azure", "Docker", "Large Language Models", "LLMs", "Claude Code", "Kubernetes", "GitHub Actions", "Dynamics 365", "Grafana", "Express.js", "NestJS", "React", "GraphQL", "MongoDB", "PostgreSQL", "MySQL"]
FULL_REMOTE_KEYWORDS: list[str] = ["100% Remote", "Fully Remote", "Full Remote", "Vollständig remote"]
HYBRID_KEYWORDS: list[str] = ["Hybrid", "mobiles Arbeiten", "Homeoffice möglich", "inklusive Homeoffice"]
REMOTE_KEYWORDS: list[str] = ["Remote"]
ONSITE_KEYWORDS: list[str] = ["On Site", "On-site", "Onsite", "vor Ort", "Präsenz", "beim Kunden"]

def contains_word(text: str, word: str) -> bool:
    pattern = rf"(?<!\w){re.escape(word)}(?!\w)"
    if re.search(pattern, text, re.IGNORECASE):
        return True
    return False

def load_ads(folder: Path) -> dict[str, str]:
    """Map file name to text for every .txt file in folder."""

    if not folder.is_dir():
        raise FileNotFoundError(f"No folder found at {folder}")

    files_list = sorted(folder.glob("*.txt"))

    job_ads: dict[str, str] = {}

    for file in files_list:
        file_content = file.read_text(encoding="utf-8")

        job_ads[file.name] = file_content
    return job_ads

def find_keywords(text: str, keywords: list[str]) -> list[str]:
    found_keywords: list[str] = []
    for keyword in keywords:
        if contains_word(text, keyword):
            found_keywords.append(keyword)
    return found_keywords

def guess_remote(text:str) -> str:
    if find_keywords(text, FULL_REMOTE_KEYWORDS):
            return "full remote"

    if find_keywords(text, HYBRID_KEYWORDS):
        return "hybrid"
    
    if find_keywords(text, REMOTE_KEYWORDS):
        return "remote"

    if find_keywords(text, ONSITE_KEYWORDS):
        return "onsite"
    
    return "unknown"

if __name__ == "__main__":
    ads_dict = load_ads(Path("data/ads"))

    for file_name, content in ads_dict.items():
        print(file_name, find_keywords(content, LANGUAGES))
        print(file_name, find_keywords(content, FRAMEWORKS))
        print(file_name, guess_remote(content))
