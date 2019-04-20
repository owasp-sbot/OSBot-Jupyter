echo "*****************************"
echo "*** Building docker image ***"
echo "*****************************"


docker build --no-cache -t local/jupyter .        || exit 1


docker run -it local/jupyter