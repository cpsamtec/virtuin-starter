FROM python:3

WORKDIR /usr/src/app 
COPY run.py . 

#Just wait for the process to be exec'd by the virtuin gui 
#Specify how the process should be exectued in the collection.py 
CMD ['bash', '-c', 'trap : TERM INT; sleep infinity & wait']

