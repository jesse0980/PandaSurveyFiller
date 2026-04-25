FROM public.ecr.aws/lambda/python:3.11

RUN pip install --no-cache-dir playwright
RUN playwright install chromium

COPY handler.py .

CMD ["handler.handler"]