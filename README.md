# TOPSIS Analysis Tool - Streamlit Version

A Streamlit web application for performing TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) analysis.

## Features

- Upload CSV data files
- Configure weights and impacts
- Instant TOPSIS analysis
- Download results as CSV
- Email results directly to your inbox
- Modern, user-friendly interface

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app locally:
```bash
streamlit run streamlit_app.py
```

## Usage

1. **Upload CSV**: Select your TOPSIS decision matrix CSV file
2. **Enter Weights**: Comma-separated values (will be normalized automatically)
3. **Enter Impacts**: Use `+` for benefit criteria, `-` for cost criteria
4. **Email Address**: Provide your email to receive results
5. **Run Analysis**: Click the "Run TOPSIS Analysis" button
6. **Download/Share**: Download results or send via email

## File Structure

```
.
├── streamlit_app.py          # Main Streamlit application
├── app.py                    # Legacy Flask app
├── topsisalgorithm.py        # TOPSIS algorithm implementation
├── TopsisAlgorithm.ipynb     # Jupyter notebook version
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── uploads/                 # Uploaded files directory
├── results/                 # Result files directory
├── static/                  # Static files (CSS, JS)
├── templates/               # HTML templates
└── README.md               # This file
```

## Requirements

- Python 3.8+
- See `requirements.txt` for all dependencies

## License

MIT

## Author

Krish Mahajan
