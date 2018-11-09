# Jupyter connected to spark locally.

Run the following commands (docker container is required).
In this case the project name (and main project folder is recommender-systems)
```commandline
docker pull jupyter/pyspark-notebook:latest
docker run --rm --name local_spark -v {path_to_your_working_dir}/recommender-systems:/opt/project/recommender-systems -p 8888:8888 jupyter/pyspark-notebook
```

```commandline
[I 10:01:56.049 NotebookApp] JupyterLab extension loaded from /opt/conda/lib/python3.6/site-packages/jupyterlab
[I 10:01:56.049 NotebookApp] JupyterLab application directory is /opt/conda/share/jupyter/lab
[I 10:01:56.084 NotebookApp] Serving notebooks from local directory: /home/jovyan
[I 10:01:56.084 NotebookApp] The Jupyter Notebook is running at:
[I 10:01:56.084 NotebookApp] http://(758690d10c86 or 127.0.0.1):8888/?token=64c17df16649f7b30e43fbd3bfb99d25139849a0968a5d3a
[I 10:01:56.085 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 10:01:56.086 NotebookApp]
```
![Jupyter on notebooks](assets/markdown-img-paste-20181109111528995.png)

Now you can open the url http://127.0.0.1:8888/?token=64c17df16649f7b30e43fbd3bfb99d25139849a0968a5d3a (mind you, he token changes all the times)
