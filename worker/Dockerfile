FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy

# Lambda expects code in /var/task
WORKDIR /var/task

# Copy handler
COPY app.py .

# Install Lambda runtime interface
RUN pip install --no-cache-dir awslambdaric playwright==1.58.0

# Lambda entrypoint
ENTRYPOINT ["python", "-m", "awslambdaric"]
CMD ["app.handler"]