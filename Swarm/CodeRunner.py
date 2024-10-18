import os
import asyncio
import logging
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import CosineStrategy
import dotenv
from openai import OpenAI
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json
import re
from swarm import Agent
from playwright.async_api import async_playwright

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
dotenv.load_dotenv(dotenv_path="kaas.env")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to create a folder for the website
def create_website_folder(url):
    domain = urlparse(url).netloc
    folder_name = domain.split('.')[0]
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

# Function to scrape a website using Crawl4AI
async def scrape_website(url):
    """
    Scrape a website using Crawl4AI's AsyncWebCrawler and clean the content.
    """
    logging.info(f"Scraping website: {url}")
    folder_name = create_website_folder(url)
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url=url)
        print(result.html)
        
    
    # Clean and structure the content
    soup = BeautifulSoup(result.html, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get text
    text = soup.get_text()
    
    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    # Remove excessive newlines
    text = re.sub(r'\n+', '\n\n', text)
    
    print(f"[DEBUG] Text : {text}")
    
    # Save the cleaned content to a file
    content_file = os.path.join(folder_name, "full_website_content.md")
    with open(content_file, "w", encoding="utf-8") as f:
        f.write(text)
    
    logging.info(f"Cleaned website content saved to {content_file}")
    
    # Save the extracted content to a file
    extracted_content_file = os.path.join(folder_name, "website-content.md")
    with open(extracted_content_file, "w", encoding="utf-8") as f:
        f.write(result.extracted_content)
    
    logging.info(f"Extracted content saved to {extracted_content_file}")
    
    return text, result.extracted_content

# Function to generate completions using OpenAI
def generate_completion(role, task, content):
    """
    Generate a completion using OpenAI's GPT model.
    This function demonstrates how to interact with OpenAI's API.
    """
    logging.info(f"Generating completion for {role}")
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Using GPT-4o for high-quality responses
        messages=[
            {"role": "system", "content": f"You are a {role}. {task}"},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content

# Function to analyze website content
def analyze_website_content(content):
    """
    Analyze the scraped website content using OpenAI.
    This function demonstrates how to use AI for content analysis.
    """
    logging.info("Analyzing website content")
    analysis = generate_completion(
        "marketing analyst",
        "Analyze the following website content and provide key insights for code development strategy.",
        content
    )
    return {"analysis": analysis}

# Function to create a coding outline
def create_coding_outline(target_audience, goals):
    """
    Create a coding outline based on target audience and goals using OpenAI.
    This function demonstrates AI's capability in strategic planning.
    """
    logging.info("Creating coding outline")
    coding_outline = generate_completion(
        "coding strategist",
        "Create an innovative coding outline based on the target audience and goals provided.",
        f"Target Audience: {target_audience}\nGoals: {goals}"
    )
    return {"coding_outline": coding_outline}

# Function to generate marketing copy
def generate_copy(brief):
    """
    Generate coding instructions based on a brief using OpenAI.
    This function shows how AI can be used for content creation.
    """
    logging.info("Generating coding instructions")
    coding_instructions = generate_completion(
        "coding writer",
        "Create compelling step by step coding instructions based on the following brief.",
        brief
    )
    return {"coding_instructions": coding_instructions}

# Define Swarm agents
class WebScraperAgent(Agent):
    async def run(self, url):
        return await scrape_website(url)

class AnalystAgent(Agent):
    async def run(self, content):
        return analyze_website_content(content)

class CampaignIdeaAgent(Agent):
    async def run(self, target_audience, goals):
        return create_coding_outline(target_audience, goals)

class CopywriterAgent(Agent):
    async def run(self, brief):
        return generate_copy(brief)

class UserInterfaceAgent(Agent):
    async def run(self):
        
        # Human input1: Give the documentation URL
        url = input("Please enter documentation URL to analyze: ")
        
        scraper_agent = WebScraperAgent()
        scraped_content, structured_content = await scraper_agent.run(url)
        
        folder_name = create_website_folder(url)
        
        analyst_agent = AnalystAgent()
        analysis = await analyst_agent.run(structured_content if structured_content else scraped_content)
        
        # Save analysis
        with open(os.path.join(folder_name, "analysis.md"), "w", encoding="utf-8") as f:
            f.write(analysis['analysis'])
        
        target_audience = input("Please describe the target audience: ")
        goals = input("Please describe the coding goals: ")
        
        campaign_agent = CampaignIdeaAgent()
        coding_outline = await campaign_agent.run(target_audience, goals)
        
        # Save coding outline
        with open(os.path.join(folder_name, "coding_outline.md"), "w", encoding="utf-8") as f:
            f.write(coding_outline['coding_outline'])
        
        copywriter_agent = CopywriterAgent()
        coding_instructions = await copywriter_agent.run(coding_outline['coding_outline'])
        
        # Save coding instructions
        with open(os.path.join(folder_name, "coding_instructions.md"), "w", encoding="utf-8") as f:
            f.write(coding_instructions['coding_instructions'])
        
        # Create and save comprehensive coding plan
        coding_plan = f"""# Comprehensive Coding Plan

## Website Analysis
{analysis['analysis']}

## Coding Outline
{coding_outline['coding_outline']}

## Coding Instructions
{coding_instructions['coding_instructions']}
"""
        with open(os.path.join(folder_name, "coding-plan.md"), "w", encoding="utf-8") as f:
            f.write(coding_plan)
        
        print(f"All output files have been saved in the '{folder_name}' folder.")
        print("Demo completed. Thank you for using our coding assistant!")
        print("Thank you for using the Stride Swarm AI Agent - to have our team implement AI agents into your business, book a call at https://executivestride.com/apply")

# Main execution
async def main():
    ui_agent = UserInterfaceAgent()
    await ui_agent.run()

if __name__ == "__main__":
    asyncio.run(main())
