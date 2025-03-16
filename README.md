# Medical Device Classification Assistant

A web application that helps classify medical devices according to FDA regulations and provides appropriate testing requirements and methods.

## Features

- Determines FDA device classification (Class I, II, or III)
- Identifies required metrics and measurement equipment
- Lists applicable general and special controls
- Provides required testing methods according to FDA regulations
- Suggests relevant standards (ISO, ASTM, etc.)

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd medical-device-classifier
```

2. Create a virtual environment and activate it:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Unix or MacOS
python -m venv venv
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the Flask application:
```bash
python example.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Enter the name of the medical device you want to classify

4. Review the classification and testing requirements provided

## Important Note

This tool provides general guidance based on FDA regulations. Always consult with regulatory experts and refer to official FDA documentation for final decisions.

## Security

- The `.env` file containing your API key is excluded from Git
- Never commit sensitive information to the repository
- Keep your API key secure and rotate it regularly

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 