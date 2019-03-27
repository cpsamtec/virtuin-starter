FROM python:3.7


WORKDIR /usr/src/app
RUN pip install --upgrade pip && pip install requests
COPY run.py .

#Just wait for the process to be exec'd by the virtuin gui
#Specify how the process should be exectued in the collection.py
CMD ['bash', '-c', 'trap : TERM INT; sleep infinity & wait']
