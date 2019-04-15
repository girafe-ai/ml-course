# Machine Learning at MIPT
Main repository for machine learning course at MIPT. All the learning materials are available here.

[ru] Informal "aggregation" of all topics by previous years students: [file](https://github.com/ml-mipt/ml-mipt/blob/master/ML_informal_notes.pdf).
This file will be updated in future.

If conda/pip doesn't work, consider using Docker.
Due to the root privileges in the docker contaner we do not recommend to use it in open networks, it may make your systerm vulnerable. The instructions will be updated in future.

1. Install Docker CE from the [official site](https://www.docker.com/products/docker-desktop)
2. In your command line run: 
```bash
sudo docker run -d -p 4545:4545 -v <your_local_path>:/home/user vlasoff/ds jupyter notebook
```
3. Open your browser on `localhost:4545`

This section will be updated and extended - stay tuned!
