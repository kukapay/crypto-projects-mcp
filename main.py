import json
import httpx
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
import locale

# Initialize the MCP server
mcp = FastMCP("CryptoProjects")

# Tool to fetch project data from Mobula API
@mcp.tool()
async def get_project_data(token_symbol: str) -> dict:
    """
    Fetch cryptocurrency project data from Mobula API.
    
    Args:
        token_symbol (str): The symbol of the cryptocurrency token (e.g., 'BTC', 'ETH')
    
    Returns:
        dict: Raw JSON response from Mobula API containing project details
    """
    async with httpx.AsyncClient() as client:
        try:
            # Construct API URL with token symbol
            url = f"https://production-api.mobula.io/api/1/metadata?asset={token_symbol}"
            response = await client.get(url)
            response.raise_for_status()  # Raise exception for non-200 status
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"API request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

# Prompt to format project data as Markdown
@mcp.prompt()
def format_project_data(token_symbol: str, lang: str = None) -> list[base.UserMessage]:
    """
    Format cryptocurrency project data into a Markdown document.
    
    Args:
        token_symbol (str): The symbol of the cryptocurrency token to fetch and format
        lang (str, optional): Language for formatting (e.g., 'en_US', 'zh_CN'). Defaults to None, using system locale.
    
    Returns:
        list[UserMessage]: Messages containing formatted Markdown content
    """
    # Use system locale if lang is not specified
    language = lang if lang else locale.getlocale()[0] or 'en_US'
    
    return [
        base.UserMessage(
            f"""
            Fetch project data for {token_symbol} using the get_project_data tool and format it as a Markdown document in {language} with the following structure:
            
            # {token_symbol} Project Information
            
            ## Overview
            - **Name**: [Project name]
            - **Symbol**: {token_symbol}
            - **Chain**: [Blockchain name]
            - **Contract Address**: [Contract address]
            - **Audit Report**: [Audit report URL or status]
            - **Description**: [Project description]
            
            ## Market Data
            - **Price**: [Current price in USD]
            - **Market Cap**: [Market capitalization in USD]
            - **Volume (24h)**: [24-hour trading volume in USD]
            - **Total Supply**: [Total token supply]
            - **Circulating Supply**: [Circulating token supply]
            
            ## Links
            - **Website**: [Project website URL]
            - **Twitter**: [Twitter URL]
            - **Discord**: [Discord URL]
            
            ## Investors
            - **Lead Investor**: [Yes/No]
            - **Name**: [Investor name]
            - **Type**: [Investor type, e.g., VC, Angel]
            - **Description**: [Brief investor description]
            
            ## Exchanges
            - [Exchange name]: [Trading pair or URL]
            
            ## Token Distribution
            - [Category, e.g., Team, Community]: [Percentage or amount]
            
            ## Token Release Schedule
            - [Date or Period]: [Amount or percentage released]
            
            If any field is unavailable, use 'Not available'. Ensure the output is formatted in {language}.
            """
        )
    ]

if __name__ == "__main__":
    mcp.run()
