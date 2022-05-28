FROM python:3.9

RUN useradd -ms /bin/bash user
USER user

COPY . /home/user/app/
WORKDIR /home/user/app
RUN pip install --user -r envs/api.txt

CMD make run
