# Use an official Python runtime as a parent image
FROM python:3.9

# Set up a non-root user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file
COPY --chown=user ./requirements.txt requirements.txt

# Install required Python packages
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the application code
COPY --chown=user . /app

# Expose the correct port (Hugging Face expects port 80)
EXPOSE 80

# Run the FastAPI app with explicit host, port, and root-path
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80", "--root-path", "/"]
