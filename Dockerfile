# Builder: resolve deps and install them into a target dir (no .venv) so they
# sit directly under ${LAMBDA_TASK_ROOT} in the runtime image.
FROM public.ecr.aws/lambda/python:3.12 AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /tmp/build
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv export --locked --no-dev --format requirements-txt --no-emit-project --output-file requirements.txt && \
    uv pip install --python /var/lang/bin/python3.12 --target /tmp/install --requirement requirements.txt

# Runtime: AWS Lambda Python 3.12 base image. Its ENTRYPOINT runs the Lambda
# Runtime Interface Client and interprets CMD as the handler ref. For local dev
# (docker-compose) we override entrypoint/command to run uvicorn instead.
FROM public.ecr.aws/lambda/python:3.12
ENV PYTHONPATH=${LAMBDA_TASK_ROOT}
ENV PATH=${LAMBDA_TASK_ROOT}/bin:$PATH
COPY --from=builder /tmp/install ${LAMBDA_TASK_ROOT}
COPY app ${LAMBDA_TASK_ROOT}/app
CMD ["app.main.handler"]
