FROM python:3.11-slim
RUN useradd -ms /bin/bash shiphydro
USER shiphydro
WORKDIR /home/shiphydro
RUN mkdir -p /home/shiphydro/mock-openfoam
CMD ["sleep", "infinity"]
