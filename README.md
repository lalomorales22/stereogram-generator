# Stereogram Generator

A Python application for creating stereograms with AI support.
<img width="1249" alt="Screenshot 2025-03-02 at 1 05 51 PM" src="https://github.com/user-attachments/assets/87d26c18-c92d-4209-a448-183d10d3ba50" />

## Features

- Create stereograms from depth maps and patterns
- Generate depth maps and patterns using Stability AI
- Hide secret messages in your stereograms
- Extract hidden messages from stereograms
- Export in PNG or JPEG format

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/stereogram-generator.git
cd stereogram-generator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Using Stability AI Integration

This application supports two methods for AI image generation:

### Method 1: Stability SDK (Recommended)

The application will first attempt to use the official Stability SDK, which provides the most reliable results:

```bash
pip install stability-sdk
```

### Method 2: REST API Fallback

If the SDK is not available, the application will fall back to using the REST API:

```bash
pip install requests pillow numpy
```

## API Key Setup

1. Get a Stability AI API key from [DreamStudio](https://dreamstudio.ai/account)
2. Enter your API key in the application's settings panel

## Usage

1. Run the application:
```bash
python app.py
```

2. Either:
   - Load a depth map and pattern image from your computer
   - Generate a depth map or pattern using the AI tab

3. Adjust the stereogram settings to your preference

4. Click "GENERATE STEREOGRAM" to create the stereogram

5. Save your stereogram with "SAVE STEREOGRAM"

## How to View Stereograms

To see the 3D effect in a stereogram:

1. Position your face close to the screen
2. Relax your eyes as if looking through the image at a distant point
3. Slowly move back while maintaining the relaxed gaze
4. The hidden 3D image should gradually appear

## Hidden Messages

The application supports hiding and extracting text messages:

1. To hide a message, enter it in the "Hidden Message" field before generating the stereogram
2. To extract a message, use the "EXTRACT HIDDEN MESSAGE" button and select a stereogram image with a hidden message

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the Stability AI team for their image generation API
- Stereogram generation technique based on various research papers in the field
