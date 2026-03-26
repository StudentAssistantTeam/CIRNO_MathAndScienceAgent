# python server
FROM python:3.13

# Docker Arg
ARG MIRROR

# Install uv
RUN pip install uv -i $MIRROR
RUN uv venv .venv

COPY . .

RUN uv sync --index-url $MIRROR
RUN chmod +x /entrypoint.sh

EXPOSE 4000
ENTRYPOINT ["./entrypoint.sh"]
