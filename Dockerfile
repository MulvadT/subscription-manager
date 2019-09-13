FROM swim-base.conda

LABEL maintainer="SWIM EUROCONTROL <http://www.eurocontrol.int>"

ENV PATH="/opt/conda/envs/app/bin:$PATH"

RUN mkdir -p /app
WORKDIR /app

COPY requirements.yml requirements.yml
RUN conda env create --name app -f requirements.yml

COPY ./subscription_manager/ ./subscription_manager/
COPY ./provision_data/ ./provision_data/

COPY . /source/
RUN set -x \
    && pip install /source \
    && rm -rf /source

CMD ["python", "/app/subscription_manager/app.py"]
