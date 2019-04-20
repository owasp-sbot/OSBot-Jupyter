FROM    jupyter/base-notebook
USER    root
RUN     wget -q https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
RUN     apt-get update
RUN     apt-get install unzip -y
RUN     unzip ngrok-stable-linux-amd64.zip

#RUN     echo "***** jupyter ****"
#RUN     jupyter -h
ADD     start-notebook.sh .
RUN     chmod +x start-notebook.sh
USER $NB_UID
#CMD     ls -la
CMD     ./start-notebook.sh