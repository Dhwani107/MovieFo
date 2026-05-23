# MovieFo

MovieFo is a small AI-powered movie information extractor. It takes a movie description as input and turns it into structured details such as title, release year, genre, director, cast, rating, and summary.

The project includes a simple Streamlit UI for entering a paragraph and viewing both the structured output and the raw model response.

Deployed link-https://moviefo.streamlit.app/

## Tech Stack
- Python
- Streamlit
- LangChain
- Mistral AI (`langchain-mistralai`)
- Pydantic
- python-dotenv

## How to Run
1. Create and activate the virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run ui.py
   ```
