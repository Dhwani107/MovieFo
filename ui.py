import html
import json

import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_mistralai import ChatMistralAI

# -------------------- Setup --------------------
load_dotenv()

@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-small-2506")

model = get_model()

# -------------------- Schema --------------------
class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str

parser = PydanticOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
Extract movie information from the paragraph.
Return a concise JSON object that matches the schema.
The summary must be a short paraphrased synopsis in 1-2 sentences.
Do not copy the input paragraph into the summary field.
Use only the information present in the paragraph, but rewrite it in your own words.
{format_instructions}
"""),
    ("human", "{paragraph}")
])

# -------------------- UI --------------------
st.set_page_config(page_title="Movie Info Extractor", page_icon="🎬", layout="centered")

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(244, 197, 100, 0.18), transparent 30%),
                radial-gradient(circle at top right, rgba(255, 122, 89, 0.12), transparent 28%),
                linear-gradient(180deg, #fffaf2 0%, #ffffff 50%, #f7f8fc 100%);
            color: #111827;
        }

        .stApp, .stApp p, .stApp span, .stApp label, .stApp div, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
            color: #111827;
        }

        .hero-card {
            background: rgba(255, 255, 255, 0.78);
            border: 1px solid rgba(20, 20, 20, 0.08);
            border-radius: 24px;
            padding: 1.5rem 1.6rem;
            box-shadow: 0 18px 50px rgba(15, 23, 42, 0.08);
            backdrop-filter: blur(14px);
        }

        .hero-kicker {
            text-transform: uppercase;
            letter-spacing: 0.18em;
            font-size: 0.74rem;
            font-weight: 700;
            color: #b45309;
            margin-bottom: 0.4rem;
        }

        .hero-title {
            font-size: 2.1rem;
            line-height: 1.1;
            margin: 0;
            color: #0f172a !important;
        }

        .hero-copy {
            margin-top: 0.7rem;
            margin-bottom: 0;
            color: #4b5563;
            font-size: 1rem;
        }

        div[data-testid="stTextArea"] textarea {
            border-radius: 18px !important;
            border: 1px solid rgba(100, 116, 139, 0.25) !important;
            padding: 1rem !important;
            background: rgba(255, 255, 255, 0.95) !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.6);
            color: #0f172a !important;
            caret-color: #0f172a !important;
        }

        div[data-testid="stTextArea"] textarea::placeholder {
            color: #94a3b8 !important;
            opacity: 1;
        }

        div[data-testid="stTextArea"] label,
        div[data-testid="stTextArea"] .st-emotion-cache-ue6h4q,
        div[data-testid="stTextArea"] .st-emotion-cache-1c7y2kd {
            color: #334155 !important;
            font-weight: 600 !important;
        }

        div[data-testid="stButton"] button {
            border: none;
            border-radius: 999px;
            padding: 0.7rem 1.2rem;
            background: linear-gradient(135deg, #f97316, #ef4444);
            color: white;
            font-weight: 700;
            box-shadow: 0 14px 30px rgba(239, 68, 68, 0.24);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }

        div[data-testid="stButton"] button:hover {
            transform: translateY(-1px);
            box-shadow: 0 18px 34px rgba(239, 68, 68, 0.3);
        }

        .soft-panel {
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 20px;
            padding: 1rem 1.1rem;
        }

        .output-card {
            background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(248,250,252,0.92));
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 18px;
            padding: 1rem;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
            height: 100%;
        }

        .field-label {
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #f97316;
            font-weight: 800;
            margin-bottom: 0.35rem;
        }

        .field-value {
            font-size: 1rem;
            color: #0f172a;
            line-height: 1.5;
            margin: 0;
        }

        .pill-list {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
        }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.75rem;
            margin: 0.25rem 0 0.9rem;
        }

        .info-grid-wide {
            display: grid;
            grid-template-columns: 1fr;
            gap: 0.75rem;
            margin: 0.25rem 0 0.9rem;
        }

        .info-card {
            border-radius: 16px;
            border: 1px solid rgba(148, 163, 184, 0.2);
            background: rgba(255, 255, 255, 0.92);
            padding: 0.85rem 0.95rem;
        }

        .info-card .card-label {
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #f97316;
            font-weight: 800;
            margin-bottom: 0.35rem;
        }

        .info-card .card-value {
            font-size: 1.15rem;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.3;
            margin: 0;
        }

        .info-card .card-value strong {
            color: #0f172a;
        }

        .info-card .card-muted {
            font-size: 0.98rem;
            font-weight: 600;
            color: #64748b;
            margin: 0;
        }

        .pill {
            display: inline-block;
            padding: 0.4rem 0.7rem;
            border-radius: 999px;
            background: rgba(249, 115, 22, 0.12);
            color: #9a3412;
            border: 1px solid rgba(249, 115, 22, 0.16);
            font-size: 0.88rem;
            font-weight: 600;
        }

        .json-box {
            background: #ffffff;
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 16px;
            padding: 1rem 1.1rem;
            overflow-x: auto;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.85);
        }

        .horizontal-bar {
            background: #ffffff;
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 16px;
            padding: 0.8rem 1rem;
            overflow-x: auto;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.85);
        }

        .horizontal-bar pre {
            margin: 0;
            color: #0f172a;
            font-size: 0.9rem;
            line-height: 1.6;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
            word-break: break-word;
        }

        .raw-grid {
            display: grid;
            grid-template-columns: minmax(140px, 180px) minmax(0, 1fr);
            gap: 0.6rem 0.9rem;
            align-items: start;
        }

        .raw-key {
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #f97316;
            font-weight: 800;
            padding-top: 0.2rem;
        }

        .raw-value {
            margin: 0;
            color: #0f172a;
            font-size: 0.95rem;
            line-height: 1.55;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
        }

        .json-box pre {
            margin: 0;
            white-space: pre-wrap;
            word-break: break-word;
            color: #0f172a;
            font-size: 0.92rem;
            line-height: 1.55;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-kicker">AI Movie Parser</div>
        <h1 class="hero-title">Movie Information Extractor</h1>
        <p class="hero-copy">Paste a movie description and convert it into structured fields like title, cast, rating, and summary.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

st.markdown("<div class='soft-panel'>", unsafe_allow_html=True)
st.caption("Tip: include plot, cast, release year, and genre details for the best extraction results.")


def render_info_card(label: str, value_html: str, muted: bool = False) -> None:
    value_class = "card-muted" if muted else "card-value"
    st.markdown(
        f'''
        <div class="info-card">
            <div class="card-label">{label}</div>
            <div class="{value_class}">{value_html}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

paragraph = st.text_area("Enter Movie Paragraph", height=200)

if st.button("Extract Data"):
    if not paragraph.strip():
        st.warning("Please enter a paragraph first.")
    else:
        with st.spinner("Analyzing movie..."):
            try:
                final_prompt = prompt.invoke({
                    "paragraph": paragraph,
                    "format_instructions": parser.get_format_instructions()
                })

                response = model.invoke(final_prompt)

                movie_data = parser.parse(response.content)

                movie_dict = movie_data.model_dump() if hasattr(movie_data, "model_dump") else movie_data.dict()
                raw_output = response.content.strip()
                if raw_output.startswith("```"):
                    raw_lines = raw_output.splitlines()
                    if len(raw_lines) >= 2 and raw_lines[-1].strip().startswith("```"):
                        raw_output = "\n".join(raw_lines[1:-1]).strip()
                    else:
                        raw_output = raw_output.strip("`")

                raw_preview = None
                try:
                    raw_preview = json.loads(raw_output)
                except Exception:
                    raw_preview = None

                st.subheader("Structured Output")
                st.markdown('<div class="output-card">', unsafe_allow_html=True)
                render_info_card("Title", html.escape(str(movie_dict.get("title") or "Not detected")), muted=not movie_dict.get("title"))

                st.markdown('<div class="info-grid">', unsafe_allow_html=True)
                render_info_card(
                    "Release Year",
                    html.escape(str(movie_dict.get("release_year") if movie_dict.get("release_year") is not None else "Not detected")),
                    muted=movie_dict.get("release_year") is None,
                )
                render_info_card(
                    "Rating",
                    html.escape(str(movie_dict.get("rating") if movie_dict.get("rating") is not None else "Not detected")),
                    muted=movie_dict.get("rating") is None,
                )
                st.markdown('</div>', unsafe_allow_html=True)

                if movie_dict.get("genre"):
                    genre_html = ''.join(f'<span class="pill">{html.escape(str(genre))}</span>' for genre in movie_dict["genre"])
                    render_info_card("Genres", f'<div class="pill-list">{genre_html}</div>')
                else:
                    render_info_card("Genres", "Not detected", muted=True)

                render_info_card(
                    "Director",
                    html.escape(str(movie_dict.get("director") or "Not detected")),
                    muted=movie_dict.get("director") is None,
                )

                if movie_dict.get("cast"):
                    cast_html = ''.join(f'<span class="pill">{html.escape(str(member))}</span>' for member in movie_dict["cast"])
                    render_info_card("Cast", f'<div class="pill-list">{cast_html}</div>')
                else:
                    render_info_card("Cast", "Not detected", muted=True)

                render_info_card(
                    "Summary",
                    html.escape(str(movie_dict.get("summary") or "Not detected")),
                    muted=movie_dict.get("summary") is None,
                )
                st.markdown('</div>', unsafe_allow_html=True)

                st.subheader("Raw Model Output")
                st.markdown('<div class="output-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
                if isinstance(raw_preview, dict):
                    raw_rows = []
                    for key, value in raw_preview.items():
                        if isinstance(value, list):
                            display_value = ", ".join(str(item) for item in value)
                        elif value is None:
                            display_value = "Not detected"
                        else:
                            display_value = str(value)
                        raw_rows.append(
                            f'<div class="raw-key">{html.escape(str(key))}</div>'
                            f'<div class="raw-value">{html.escape(display_value)}</div>'
                        )
                    st.markdown(
                        f'<div class="horizontal-bar"><div class="raw-grid">{"".join(raw_rows)}</div></div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="horizontal-bar"><pre>{html.escape(raw_output)}</pre></div>',
                        unsafe_allow_html=True,
                    )
                st.markdown('</div>', unsafe_allow_html=True)

                st.subheader("Structured JSON")
                json_text = json.dumps(movie_dict, indent=2, ensure_ascii=False)
                json_lines = json_text.splitlines()
                json_html = "".join(
                    f'<div class="json-line">{html.escape(line) if line else "&nbsp;"}</div>'
                    for line in json_lines
                )
                st.markdown(
                    f'<div class="json-box"><div class="json-lines">{json_html}</div></div>',
                    unsafe_allow_html=True,
                )

                st.success("Extraction Completed Successfully!")

            except Exception as e:
                st.error("Failed to parse response. Model did not follow schema.")
                st.exception(e)

st.markdown("</div>", unsafe_allow_html=True)