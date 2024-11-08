# build container
docker build -t bmfm-mammal-inference .

# check the exit status
if [ $? -eq 0 ]; then
    echo ">> [I] Container built successfully"
    # run container
    docker run --rm -it --name mammal -p 8080:8080 -v $HOME/.openad_models:/tmp/.openad_models bmfm-mammal-inference
else
    sleep 2
    echo ">> [E] Container build failed"
    exit 1
fi
