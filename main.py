import wikipediaapi
from fastapi import FastAPI

def collect_sections_data(sections, result_list=[]):
    for s in sections:
        result_list.append({
            "title": s.title,
            "text": s.text.strip()
        })

        if s.sections:
            collect_sections_data(s.sections, result_list)

    return result_list

app = FastAPI()

@app.get("/search-wikepedia")
async def searchWikepedia(topic, language="en"):
    try:
        wiki = wikipediaapi.Wikipedia(
            user_agent="MyKnowledgeBot/1.0 (myemail@example.com)",
            language=language
        )

        page = wiki.page(topic)

        all_sections = collect_sections_data(page.sections, [])

        if page.exists():
            return {
                "result": True,
                "content": {
                    "title": page.title,
                    "preamble": page.summary,
                    "text": page.text,
                    "sections": all_sections,
                    "fullUrl": page.fullurl
                }
            }
        else:
            print("Страница не найдена.")
            return {
                "result": True,
                "content": "Page Not Found",
                    }
    except Exception as e:
        return {
            "result": False,
            "error": e
                }