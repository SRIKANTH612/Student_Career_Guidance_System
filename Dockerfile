# Use Python 3.9 or your preferred version
FROM python:3.9

# Set the working directory
WORKDIR /code

# Copy requirements and install
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of your application code
COPY . .

# Flask typically runs on port 5000, but Hugging Face expects 7860
CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "7860"]
