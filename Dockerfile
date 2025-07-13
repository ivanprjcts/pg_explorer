FROM python:3.13.5

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set up working dir
ENV PATH="/.venv/bin:$PATH"
ENV PROJECT_DIR=/app
ENV APP_USER=appuser
ENV DJANGO_SETTINGS_MODULE=pg_explorer.settings

# Install uv and compilation dependencies
RUN pip install uv

# Install python dependencies in /.venv
COPY ./pyproject.toml ./uv.lock ./
RUN uv sync

# Create and switch to a new user
RUN useradd --create-home -d ${PROJECT_DIR} ${APP_USER}
WORKDIR ${PROJECT_DIR}

# Copy code as appuser owner
COPY --chown=${APP_USER}:${APP_USER} ./manage.py manage.py
COPY --chown=${APP_USER}:${APP_USER} ./pg_explorer pg_explorer
COPY --chown=${APP_USER}:${APP_USER} ./sample_app sample_app

USER ${APP_USER}

CMD ["python", "manage.py", "shell"]
