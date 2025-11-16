#!/bin/bash

# Start the FastAPI app using uvicorn on port 9696
uvicorn predict:app --host 0.0.0.0 --port 9696 &

# Start the Streamlit app on its default port 8501
streamlit run app.py --server.port 8501
