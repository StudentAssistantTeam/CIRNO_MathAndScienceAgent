# python server
FROM docker.xuanyuan.me/python:3.13

# Install uv
RUN pip install uv -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
RUN uv venv .venv

COPY . .

RUN uv sync --index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
RUN chmod +x /entrypoint.sh

EXPOSE 4000
ENTRYPOINT ["./entrypoint.sh"]
