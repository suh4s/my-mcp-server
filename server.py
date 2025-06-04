from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
from dice_roller import DiceRoller
import qrcode
import io
import base64
from pint import UnitRegistry
import requests
import json

load_dotenv()

mcp = FastMCP("mcp-server")
client = TavilyClient(os.getenv("TAVILY_API_KEY"))
ureg = UnitRegistry()

@mcp.tool()
def web_search(query: str) -> str:
    """Search the web for information about the given query"""
    search_results = client.get_search_context(query=query)
    return search_results

@mcp.tool()
def roll_dice(notation: str, num_rolls: int = 1) -> str:
    """Roll the dice with the given notation"""
    roller = DiceRoller(notation, num_rolls)
    return str(roller)

@mcp.tool()
def generate_qr_code(text: str, size: int = 10, border: int = 4) -> str:
    """Generate a QR code for the given text and return it as a base64 encoded image"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=border,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return f"QR Code generated successfully for: '{text}'\nBase64 image data: data:image/png;base64,{img_base64[:100]}... (truncated for display)\nUse this in an image viewer or HTML to see the QR code."
    except Exception as e:
        return f"Error generating QR code: {str(e)}"

@mcp.tool()
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """Convert between different units (e.g., temperature, length, weight, volume)"""
    try:
        # Manual temperature conversions to avoid pint offset unit issues
        from_unit_lower = from_unit.lower()
        to_unit_lower = to_unit.lower()
        
        # Temperature conversion mappings
        temp_conversions = {
            ('fahrenheit', 'celsius'): lambda f: (f - 32) * 5/9,
            ('celsius', 'fahrenheit'): lambda c: c * 9/5 + 32,
            ('celsius', 'kelvin'): lambda c: c + 273.15,
            ('kelvin', 'celsius'): lambda k: k - 273.15,
            ('fahrenheit', 'kelvin'): lambda f: (f - 32) * 5/9 + 273.15,
            ('kelvin', 'fahrenheit'): lambda k: (k - 273.15) * 9/5 + 32,
        }
        
        # Check if it's a temperature conversion FIRST
        conversion_key = (from_unit_lower, to_unit_lower)
        if conversion_key in temp_conversions:
            converted_value = temp_conversions[conversion_key](value)
            return f"{value} {from_unit} = {converted_value:.2f} {to_unit}"
        
        # Only use pint for non-temperature units
        try:
            quantity = value * ureg(from_unit)
            converted = quantity.to(to_unit)
            return f"{value} {from_unit} = {converted.magnitude:.6f} {to_unit}"
        except Exception as pint_error:
            # If pint fails, return a more helpful error message
            return f"Error converting units with pint: {str(pint_error)}\nSupported unit examples:\n- Length: meter, km, inch, foot, mile\n- Weight: gram, kg, pound, ounce\n- Temperature: celsius, fahrenheit, kelvin\n- Volume: liter, gallon, cup, milliliter"
            
    except Exception as e:
        return f"General error converting units: {str(e)}"

@mcp.tool()
def shorten_url(url: str, service: str = "tinyurl") -> str:
    """Shorten a URL using various services (tinyurl, is.gd)"""
    try:
        if service.lower() == "tinyurl":
            # Using TinyURL API
            api_url = f"http://tinyurl.com/api-create.php?url={url}"
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                shortened = response.text.strip()
                return f"Original URL: {url}\nShortened URL: {shortened}"
            else:
                return f"Error shortening URL with TinyURL: HTTP {response.status_code}"
                
        elif service.lower() == "is.gd":
            # Using is.gd API
            api_url = "https://is.gd/create.php"
            data = {"format": "simple", "url": url}
            response = requests.post(api_url, data=data, timeout=10)
            if response.status_code == 200:
                shortened = response.text.strip()
                return f"Original URL: {url}\nShortened URL: {shortened}"
            else:
                return f"Error shortening URL with is.gd: HTTP {response.status_code}"
        else:
            return f"Unsupported service: {service}. Available services: tinyurl, is.gd"
            
    except requests.RequestException as e:
        return f"Network error while shortening URL: {str(e)}"
    except Exception as e:
        return f"Error shortening URL: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")