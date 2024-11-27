# build container
podman  build -t quay.io/ibmdpdev/bmfm_mammal_properties:latest .

# check the exit status
if [ $? -eq 0 ]; then
    echo ">> [I] Container built successfully"
    # run container
    podman run --rm -it --name mammal -p 8080:8080 -v $HOME/.openad_models:/tmp/.openad_models quay.io/ibmdpdev/bmfm_mammal_properties:latest
else
    sleep 2
    echo ">> [E] Container build failed"
    exit 1
fi
