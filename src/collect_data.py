import os
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

REMOTIVE_URL = "https://api.adzuna.com/v1/api/jobs"
REQUEST_DELAY = 1.1

SEARCH_QUERIES = [
    ("Data Analyst", "Data Analyst"),
    ("Data Engineer", "Data Engineer"),
    ("BI Analyst", "BI Analyst"),
    ("Data Scientist", "Data Scientist"),
]

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = RAW_DIR / "vacancies_raw.csv"

HEADERS = {
    "User-agent": "DataCareerAnalytics/1.0",
}
# Классификация ролей (на случай, если Adzuna category не совпадает)
ROLE_PATTERNS = [
    (r"data\s*engineer|etl\s*developer|big\s*data\s*engineer", "Data Engineer"),
    (r"data\s*scientist|machine\s*learning\s*engineer|ml\s*engineer|nlp", "Data Scientist"),
    (r"bi\s*analyst|business\s*intelligence\s*analyst|bi\s*developer", "BI Analyst"),
    (r"data\s*analyst|product\s*analyst|marketing\s*analyst", "Data Analyst"),
]

def classify_role(title: str) -> str:
    title_lower = title.lower()
    for pattern, role in ROLE_PATTERNS:
        if re.search(pattern, title_lower):
            return role
    return "other"

def fetch_remotive(query: str) -> list[dict]:
    """Дополнительный сбор из Remotive (без ключа)."""
    rows: list[dict] = []
    try:
        resp = requests.get(
            "https://remotive.com/api/remote-jobs",
            params={"search": query, "limit": 100},
            headers=HEADERS,
            timeout=30,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"  [!] Ошибка Remotive ('{query}'): {exc}")
        return rows

    data = resp.json()
    for job in data.get("jobs", []):
        salary_text = job.get("salary", "")
        salary_from = salary_to = None
        currency = None
        if salary_text:
            numbers = re.findall(r"\d+[\d,]*k?", salary_text.lower().replace(",", ""))
            parsed = []
            for n in numbers:
                if n.endswith("k"):
                    parsed.append(int(float(n[:-1]) * 1000))
                else:
                    parsed.append(int(n))
            if len(parsed) >= 2:
                salary_from, salary_to = parsed[0], parsed[1]
            elif len(parsed) == 1:
                salary_from = parsed[0]
            currency = "USD"

        rows.append({
            "id": job.get("id"),
            "source": "remotive",
            "query": query,
            "title": job.get("title"),
            "company": job.get("company_name"),
            "city": job.get("candidate_required_location", "Remote"),
            "salary_from": salary_from,
            "salary_to": salary_to,
            "currency": currency,
            "experience": "",
            "published_at": job.get("publication_date"),
            "url": job.get("url"),
            "snippet_requirement": "",
            "snippet_responsibility": "",
            "description": (job.get("description") or "")[:500],
            "job_type": job.get("job_type"),
            "category": job.get("category"),
            "tags": ",".join(job.get("tags", [])),
        })

    print(f"  -> Remotive '{query}': +{len(rows)} вакансий")
    return rows

def fetch_adzuna(
        app_id: str,
        app_key: str,
        query_encoded: str,
        query_label: str,
        country: str = "ru",
        pages: int = 5,
    ) -> list[dict]:

    rows: list[dict] = []
    base_url = f"https://api.adzuna.com/v1/api/jobs/{country}/search"

    for page in range(1, pages+1):
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "what": query_encoded,
            "results_per_page": 50,
        }
        try:
            resp = requests.get(
                f"{base_url}/{page}",
                params = params,
                headers = HEADERS,
                timeout = 30,
            )
            resp.raise_for_status()
        except requests.RequestException as exc:
            print(f"  [!] Ошибка Adzuna стр. {page} ('{query_label}'):{exc}")
            continue

        data = resp.json()
        results = data.get("results", [])
        if not results:
            break

        for job in results:
            salary_raw = job.get("salary_min") or job.get("salary_max")
            salary_from = job.get("salary_min")
            salary_to = job.get("salary_max")
            
            rows.append({
                "id": job.get("id"),
                "source": f"adzuna_{country}",
                "query": query_label,
                "title": job.get("title"),
                "company": (job.get("company") or {}).get("display_name"),
                "city": (job.get("location") or {}).get("display_name"),
                "salary_from":salary_from,
                "salary_to":salary_to,
                "currency": "GBP" if salary_raw else None,
                "experience": "",
                "published_at": job.get("created"),
                "url": job.get("redirect_url"),
                "snippet_requirement": "",
                "snippet_responsibility": "",
                "description": job.get("description", "")[:500],
                "job_type": job.get("contract_type"),
                "category": (job.get("category") or {}).get("label"),
                "tags": "",
            })

        print(
            f"  -> '{query_label}' стр. {page}: +{len(results)} вакансий "
            f"(всего {len(rows)})"
        )

        time.sleep(REQUEST_DELAY)
    return rows
def main() -> None:
    print("=" * 60)
    print("Сбор реальных Data/IT-вакансий через открытые API")
    print("=" * 60)

    app_id = os.environ.get("ADZUNA_APP_ID", "")
    app_key = os.environ.get("ADZUNA_APP_KEY", "")

    all_rows: list[dict] = []

    if app_id and app_key:
        # --- Adzuna (основной источник) ---
        print("\n🌐 Adzuna API (Великобритания)")
        for query_enc, query_label in SEARCH_QUERIES:
            rows = fetch_adzuna(app_id, app_key, query_enc, query_label, country="gb", pages=5)
            all_rows.extend(rows)

        # Adzuna US
        print("\n🌐 Adzuna API (США)")
        for query_enc, query_label in SEARCH_QUERIES[:4]:
            rows = fetch_adzuna(app_id, app_key, query_enc, query_label, country="us", pages=3)
            all_rows.extend(rows)
    else:
        print("\n⚠️  ADZUNA_APP_ID / ADZUNA_APP_KEY не заданы.")
        print("   Adzuna — основной источник реальных вакансий.")
        print("   Получите бесплатные ключи за 2 минуты:")
        print("   https://developer.adzuna.com/signup")
        print()
        print("   Затем:")
        print("   export ADZUNA_APP_ID='ваш_id'")
        print("   export ADZUNA_APP_KEY='ваш_key'")
        print()
        print("   Пока собираю только через Remotive (резервный источник)...")

    # --- Remotive (дополнительный источник, всегда) ---
    print("\n🌐 Remotive API (удалённые вакансии, без ключа)")
    remotive_queries = [
        "Data Analyst",
        "Data Engineer",
        "Data Scientist",
        "BI Analyst",
        "Machine Learning Engineer",
    ]
    for query in remotive_queries:
        rows = fetch_remotive(query)
        all_rows.extend(rows)
        time.sleep(REQUEST_DELAY)

    if not all_rows:
        print("\n❌ Ни одной вакансии не собрано.")
        if not app_id:
            print("   Получите Adzuna-ключи или проверьте интернет.")
        return

    df = pd.DataFrame(all_rows)
    total_before = len(df)

    # Дедупликация
    df = df.drop_duplicates(subset=["id", "source"])
    total_after = len(df)
    duplicates = total_before - total_after

    print(f"\n{'=' * 60}")
    print(f"Собрано всего: {total_before}")
    if duplicates:
        print(f"Удалено дубликатов: {duplicates}")
    print(f"Уникальных вакансий: {total_after}")

    # Классификация
    df["role"] = df["title"].apply(classify_role)
    print("\nРаспределение по ролям:")
    for role, cnt in df["role"].value_counts().items():
        print(f"  {role}: {cnt}")

    salary_share = df["salary_from"].notna().mean() * 100
    print(f"\nВакансий с указанной зарплатой: {salary_share:.1f}%")

    sources = df["source"].value_counts()
    print("\nПо источникам:")
    for src, cnt in sources.items():
        print(f"  {src}: {cnt}")

    df.to_csv(OUT_PATH, index=False)
    print(f"\n✅ Сохранено: {OUT_PATH.resolve()}")
    print(f"   Файл готов для следующего этапа: очистка данных.")


if __name__ == "__main__":
    main()