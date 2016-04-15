### v2.0.0-beta1 -> v2.0.0-beta2

#### Features

 - [`36ea3fa`](https://github.com/deis/dockerbuilder/commit/36ea3fa8aa3f1eec31677304b2ef5caa800dcc8d) _scripts: add CHANGELOG.md and generator script
 - [`1d54179`](https://github.com/deis/dockerbuilder/commit/1d541794e8022acbac81dd37c94e10fbba412876) storage: Add support for all storage backends

#### Maintenance

 - [`2be1cac`](https://github.com/deis/dockerbuilder/commit/2be1cacfb7a0e5d4b87d55e8d9ce8966d4d4d81c) .travis.yml: run docker builds on PRs

### v2.0.0-beta1

#### Features

 - [`a18a916`](https://github.com/deis/dockerbuilder/commit/a18a9163d985934347b35504fa618b841b938bf3) travis: add traivs webhook to jenkins
 - [`c7ddccf`](https://github.com/deis/dockerbuilder/commit/c7ddccf3205e468d0ce3a881148dc9eb4b65e31b) mutable: add support for mutable image builds
 - [`0825009`](https://github.com/deis/dockerbuilder/commit/082500922b933a32c4174c4985f12e3e13ccba8a) gcs: add support for GCS storage
 - [`36a2189`](https://github.com/deis/dockerbuilder/commit/36a218979e609b5adfb55a6a99f9e2ab6c636ff4) vendor: remove vendor directory
 - [`b08ac93`](https://github.com/deis/dockerbuilder/commit/b08ac93844de77d132daafed87a0cecc9805e662) manifest: change builder name
 - [`7c1cead`](https://github.com/deis/dockerbuilder/commit/7c1cead1ab4e5ce18f39aa659280e9f9ecbf6908) region: add region to s3 client config
 - [`ce77440`](https://github.com/deis/dockerbuilder/commit/ce77440ddd6e62c2ce35804b461ca2998ae89b8c) makefile: check version flag is set
 - [`7581cc3`](https://github.com/deis/dockerbuilder/commit/7581cc340abea866eef5fd764102911e7ca2f481) makefile: remove script to change image in RC
 - [`e7a4f86`](https://github.com/deis/dockerbuilder/commit/e7a4f86f1a2fc24403264ffe536c8beae73abc59) travis: change yaml to yml
 - [`18ad157`](https://github.com/deis/dockerbuilder/commit/18ad1578cde336bf6b6cdb84537bec50fbf4400c) CI: add travis.yml and build script
 - [`1db350e`](https://github.com/deis/dockerbuilder/commit/1db350ea3de1a051be2af5045e57cc55038d93d2) dockerbuilder: builder pod that supports dockerfie builds

#### Fixes

 - [`93b33e1`](https://github.com/deis/dockerbuilder/commit/93b33e1637c52d925183fdf2d7009d4f8e3c3915) deploy.py: don't replace if string is None
 - [`2ba4626`](https://github.com/deis/dockerbuilder/commit/2ba4626188519bc8b9019a539348ba6c0cb81261) Makefile: remove duplicate "docker-build" target

#### Maintenance

 - [`0773673`](https://github.com/deis/dockerbuilder/commit/0773673ee5266fc4883497006c129f6645b71e2b) Dockerfile: update docker-py to 1.7.2
 - [`274660c`](https://github.com/deis/dockerbuilder/commit/274660ce6bfaf589adcd6350ce4db8b85a2de363) requirements: update docker-py to 1.7.0
