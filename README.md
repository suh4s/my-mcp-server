<p align = "center" draggable="false" ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719" 
     width="200px"
     height="auto"/>
</p>

## <h1 align="center" id="heading">Custom MCP Server with Enhanced Tools</h1>

This project demonstrates a powerful MCP (Model Context Protocol) server with **5 custom tools** that extend AI assistant capabilities directly in Cursor. Built on the foundation of the AI Makerspace MCP framework, this server includes web search, utility tools, and content generation capabilities.

## 🚀 Features

### **Available Tools:**

🔍 **Web Search** - Search the web using Tavily API integration  
🎲 **Dice Roller** - Roll dice with custom notation (e.g., `2d20k1`)  
📱 **QR Code Generator** - Generate QR codes for any text or URL  
🔄 **Unit Converter** - Convert between different units (length, weight, temperature, volume)  
🔗 **URL Shortener** - Shorten URLs using TinyURL or is.gd services  

## Project Overview

The MCP server integrates seamlessly with Cursor through the Model Context Protocol, providing instant access to powerful tools directly within your AI assistant. The server is designed to run in standard input/output (stdio) transport mode and includes:

- **TavilyClient**: Web search capabilities using the Tavily API
- **QR Code Generation**: Base64 encoded QR codes using the `qrcode` library
- **Unit Conversion**: Comprehensive unit conversion with manual temperature handling
- **URL Shortening**: Multiple service support (TinyURL, is.gd)
- **Dice Rolling**: Advanced dice notation with keep-highest functionality

## Prerequisites

- Python 3.13 or higher
- A valid Tavily API key
- UV package manager (for dependency management)

## ⚠️NOTE FOR WINDOWS:⚠️

You'll need to install this on the *Windows* side of your OS. 

This will require getting two CLI tool for Powershell, which you can do as follows:

- `winget install astral-sh.uv`
- `winget install --id Git.Git -e --source winget`

After you have those CLI tools, please open Cursor *into Windows*.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/suh4s/my-mcp-server.git
   cd my-mcp-server
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Configure environment variables**:
   Create a `.env` file and add your Tavily API key:
   ```
   TAVILY_API_KEY=your_api_key_here
   ```

## Running the MCP Server

To start the MCP server, you will need to add the following to your MCP Profile in Cursor:

> NOTE: To get to your MCP config, use the Command Palette (CMD/CTRL+SHIFT+P) and select "View: Open MCP Settings" and replace the contents with the JSON configuration below.

```json
{
    "mcpServers": {
        "mcp-server": {
            "command": "uv",
            "args": ["--directory", "/FULL/PATH/TO/YOUR/REPOSITORY", "run", "server.py"]
        }
    }
}
```

The server will start and listen for commands via standard input/output.

## 🛠️ Tool Usage Examples

### **QR Code Generator**
```
"Generate a QR code for 'Hello World'"
"Create a QR code for https://github.com/suh4s/my-mcp-server"
```

### **Unit Converter**
```
"Convert 100 fahrenheit to celsius"
"Convert 5 miles to kilometers"
"Convert 2 pounds to grams"
```

### **URL Shortener**
```
"Shorten this URL: https://github.com/suh4s/my-mcp-server"
"Shorten https://example.com using is.gd"
```

### **Dice Roller**
```
"Roll 2d20k1" (roll 2 20-sided dice, keep highest)
"Roll 3d6" (roll 3 6-sided dice)
```

### **Web Search**
```
"Search for 'MCP protocol documentation'"
"Find recent AI news"
```

## 🔧 Technical Implementation

### **Dependencies:**
- `mcp[cli]` - Model Context Protocol framework
- `tavily-python` - Web search API integration
- `qrcode` + `pillow` - QR code generation
- `pint` - Unit conversion library
- `requests` - HTTP requests for URL shortening
- `python-dotenv` - Environment variable management

### **Architecture:**
- **FastMCP Server**: Handles tool registration and protocol communication
- **Tool Functions**: Decorated with `@mcp.tool()` for automatic discovery
- **Error Handling**: Comprehensive error handling with helpful messages
- **Type Safety**: Full type hints for all tool parameters

## 🎯 Advanced Features

- **Temperature Conversion**: Custom formulas to handle Fahrenheit/Celsius conversions
- **QR Code Customization**: Adjustable size and border parameters
- **Multiple URL Services**: TinyURL and is.gd support with fallback handling
- **Dice Notation**: Support for complex dice expressions with keep-highest logic

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## Acknowledgments

Built as part of the AI Makerspace MCP Session. Original framework by [AI-Maker-Space](https://github.com/AI-Maker-Space/MCP-Session-Code).
