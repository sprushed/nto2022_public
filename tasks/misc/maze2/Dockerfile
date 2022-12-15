FROM python:3.10-buster

RUN mkdir /app
RUN pip install pipenv
COPY ./Pipfile ./Pipfile.lock /app/
WORKDIR /app
RUN pipenv install --system

COPY ./ /app/
RUN useradd -m user && chown -R user:user /app

WORKDIR /app

USER user

CMD ["python", "maze.py"]
