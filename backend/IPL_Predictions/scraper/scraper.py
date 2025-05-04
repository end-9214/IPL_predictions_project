import asyncio
from crawl4ai import AsyncWebCrawler
import os

async def main():
    # url = "https://www.espncricinfo.com/series/ipl-2025-1449924/match-schedule-fixtures-and-results"
    url = "https://www.cricbuzz.com/cricket-series/9237/indian-premier-league-2025/matches"

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)

        # Save the HTML content to file
        output_dir = "ipl2024-stats"
        os.makedirs(output_dir, exist_ok=True)

        # Optionally save Markdown or plaintext
        markdown_path = os.path.join(output_dir, "page.md")
        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(result.markdown)

        print(f"✅ Page scraped and saved to:{markdown_path}")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
