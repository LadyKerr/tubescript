# TubeScript 📝

TubeScript is a Python application that fetches the transcript of a YouTube video and saves it to a text file. It provides both a command-line interface and a user-friendly web interface using Streamlit.

## Features

- Extract transcripts from YouTube videos
- Save transcripts to text files in a designated folder
- Web interface for easy interaction

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tubescript.git
   cd tubescript
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Web Interface

Run the Streamlit app:

```bash
streamlit run tubescript/app.py
```

Then open your web browser and navigate to `http://localhost:8501` to access the TubeScript web interface.

### Command-Line Interface

To use the command-line interface, run the following command:

```bash
python tubescript/utils.py <youtube_url>
```

Replace `<youtube_url>` with the URL of the YouTube video for which you want to fetch the transcript.

## License

[MIT](https://choosealicense.com/licenses/mit/)