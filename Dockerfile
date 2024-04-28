FROM continuumio/anaconda3

WORKDIR /app


COPY . .
COPY environment.yml /tmp/environment2.yml

RUN conda env create -f /tmp/environment2.yml

CMD ["conda", "run", "-n", "env", "python", "main.py"]

CMD ["git", "clone", "https://github.com/xinntao/Real-ESRGAN.git"]
CMD ["cd", "Real-ESRGAN"]

RUN pip install basicsr \
    && pip install facexlib \
    && pip install gfpgan

COPY requirements.txt /app/
RUN pip install -r requirements.txt
RUN pip install pytorch
RUN pip install torchfile
RUN pip install torchvision==0.14.0

RUN python setup.py develop

CMD ["cd", ".."]
RUN apt-get update && apt-get install -y wget

# Create a directory for weights
RUN mkdir weights


RUN wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -P weights

