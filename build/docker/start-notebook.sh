echo "**** starting notebook****"
./ngrok http 8888 > /dev/null &

jupyter notebook

