import asyncio
import os
from mcp_server import scrape_github, analyze_profile, generate_card_html, save_card
from dotenv import load_dotenv

load_dotenv()

async def test_end_to_end():
    username = "torvalds"
    print(f"--- Testing for user: {username} ---")
    
    try:
        # 1. Scrape GitHub
        print("1. Scraping GitHub...")
        github_data = await scrape_github(username)
        if "error" in github_data:
            print(f"Error scraping GitHub: {github_data['error']}")
            return
        print(f"Successfully scraped {github_data['name']}")

        # 2. Analyze Profile
        print("2. Analyzing profile with Gemini...")
        analysis = await analyze_profile(github_data)
        print("Analysis complete.")

        # 3. Generate HTML
        print("3. Generating HTML card...")
        html = await generate_card_html(username, github_data, analysis)
        print("HTML generation complete.")

        # 4. Save and Print results
        print("\n--- Results ---")
        print(f"Card Theme: {analysis.get('card_theme')}")
        print(f"Developer Vibe: {analysis.get('developer_vibe')}")
        
        # Save card for completeness
        path = await save_card(username, html)
        print(f"Card saved to: {path}")

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_end_to_end())
