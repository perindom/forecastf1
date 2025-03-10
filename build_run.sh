docker build -t drl .
docker run --rm -it \
    -p 8888:8888 \
    --user=root \
    --env="DISPLAY" \
    --workdir=/main \
    --volume="$PWD":/main \
    drl /bin/bash
