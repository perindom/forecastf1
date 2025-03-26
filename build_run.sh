<<<<<<< HEAD
docker build -t aml .
=======
docker build -t drl .
>>>>>>> 12a71fdcc31b93707638f511eab4bf4883356c5c
docker run --rm -it \
    -p 8888:8888 \
    --user=root \
    --env="DISPLAY" \
    --workdir=/main \
    --volume="$PWD":/main \
<<<<<<< HEAD
    aml /bin/bash
=======
    drl /bin/bash
>>>>>>> 12a71fdcc31b93707638f511eab4bf4883356c5c
