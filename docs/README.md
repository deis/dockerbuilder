# dockerbuilder

`dockerbuilder` is a simple tool for downloading slugs and executing Docker builds. It's most commonly launched as a pod from [builder](https://github.com/deis/builder) to build a Dockerfile codebase, but it's generic and can be configured for use anywhere.

It has a single command, `run`, which does the following (you can get a similar description by running `help`):

1. Calls `mc cp` to download `$TAR_URL` to a temporary directory (`/tmp` hereafter). Assumes `$TAR_URL` points to a gzipped tarball (`.tar.gz`)
2. Runs `tar xvzf` inside `/tmp` to unzip the downloaded tarball
3. Runs `docker build -t $IMG_URL .` in `/tmp` to build the Docker image
4. Runs `docker push $IMG_URL`
