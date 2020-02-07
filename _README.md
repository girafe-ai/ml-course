# Machine Learning at MIPT

Main repository for machine learning course at MIPT.
All the learning materials are available here.

## Video lectures

* Previous term (__basic track__) lectures are available on [youtube playlist](https://www.youtube.com/playlist?list=PL4_hYwCyhAvasRqzz4w562ce0esEwS0Mt)

* Current launch (__advanced track__) lectures (WIP): [youtube playlist](https://www.youtube.com/playlist?list=PL4_hYwCyhAvZeq93ssEUaR47xhvs7IhJM)

* Current launch (__advanced track__) seminars (WIP): [youtube playlist](https://www.youtube.com/playlist?list=PL4_hYwCyhAvYvuHz_PKlEV-kOsK2bwUBg)

## Prerequisites

We are expecting our students to have a basic knowlege of:
* calculus, especially matrix calculus
* probability theory and statistics
* programming, especially on Python

Although if you don't have any of this, you could substitude it with your diligence because the course provides additional materials to study requirements yourself.

## Theoretical materials

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
