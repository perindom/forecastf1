docker build -t ff1 .
docker run --rm -it \
    -p 8888:8888 \
    --user=root \
    --env="DISPLAY" \
    --workdir=/main \
    --volume="$PWD":/main \
    ff1 /bin/bash
