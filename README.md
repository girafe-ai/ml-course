# Machine Learning at MIPT
This course aims to introduce students to contemporary state of Machine Learning and Artificial Intelligence. It is designed to take one year (two terms at MIPT) - approximately 2 * 15 lectures and seminars.

All materials are available here, the complementary website available at [`ml-mipt.github.io`](https://ml-mipt.github.io/)

## `Important` current repository structure

* on `master` branch previous term materials are stored
    to give a quick and comprehensive overview
* on `basic` and `advanced` branches materials for
    current launches are being published

Later (after the term ends) we will merge a new state to master as `fall_2019`.

## Current launches

As of Fall 2019 we have two tracks: [`basic`](basic.md) and [`advanced`](advanced.md).

## Video lectures

* basic track (Spring 2019): [`youtube playlist`](https://www.youtube.com/playlist?list=PL4_hYwCyhAvasRqzz4w562ce0esEwS0Mt)
* advanced track (Fall 2019, in progress): [`youtube playlist`](https://www.youtube.com/playlist?list=PL4_hYwCyhAvZeq93ssEUaR47xhvs7IhJM)

## Prerequisites

We are expecting our students to have a basic knowlege of:
* calculus, especially matrix calculus
* probability theory and statistics
* programming, especially on Python

Although if you don't have any of this, you could substitude it with your diligence because the course provides additional materials to study requirements yourself.

## Theoretical and extra materials

Informal "aggregation" of all topics by previous years students: [file](https://github.com/ml-mipt/ml-mipt/blob/master/ML_informal_notes.pdf) (in Russian).

## Docker image

If conda/pip doesn't work, consider using Docker.
Due to the root privileges in the docker contaner we do not recommend to use it in open networks, it may make your systerm vulnerable. The instructions will be updated in future.

1. Install Docker CE from the [official site](https://www.docker.com/products/docker-desktop)
2. In your command line run: 
```bash
sudo docker run -d -p 4545:4545 -v <your_local_path>:/home/user vlasoff/ds jupyter notebook
```
3. Open your browser on `localhost:4545`
