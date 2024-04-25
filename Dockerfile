FROM continuumio/anaconda3

WORKDIR /app


COPY . .
COPY environment.yml /tmp/environment2.yml

RUN conda env create -f /tmp/environment2.yml

CMD ["conda", "run", "-n", "env", "python", "main.py"]
