from playwright.sync_api import sync_playwright

def search_candidates_google(job_title, skills):
    query = f"site:linkedin.com/in {job_title} " + " ".join(skills)
    print(f"\n🔍 Searching: {query}")
    links = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=False to visually debug
        page = browser.new_page()
        page.goto(f"https://duckduckgo.com/?q={query}", timeout=60000)

        # Wait for result links with longer timeout
        try:
            page.wait_for_selector("a[data-testid='result-title-a']", timeout=15000)
        except Exception as e:
            print(f"❌ Error during search: {e}")
            browser.close()
            return []

        # Grab result links
        anchors = page.query_selector_all("a[data-testid='result-title-a']")
        for anchor in anchors:
            href = anchor.get_attribute("href")
            if "linkedin.com/in" in href:
                links.append(href)

        browser.close()

    return links
