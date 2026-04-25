FROM mcr.microsoft.com/playwright/python:v1.41.2-jammy

# Lambda expects code in /var/task
WORKDIR /var/task

# Copy handler
COPY handler.py .

# Install Lambda runtime interface
RUN pip install --no-cache-dir awslambdaric

# Lambda entrypoint
ENTRYPOINT ["python", "-m", "awslambdaric"]
CMD ["handler.handler"]