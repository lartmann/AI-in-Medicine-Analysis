# Overview

This project performs a small data analysis of scientific publications in the subfield of artificial intelligence in medicine. The results are described in a short article which can be found in `article.pdf`. The data assembly and creation of visualizations is described and performed in the `analysis.ipynb` notebook. 

In order to retrieve the relevant data, a few steps are needed:
1. Download the meta data of the papers since 2019 through the [OpenAlex](https://docs.openalex.org/how-to-use-the-api/api-overview) API and save them in csv files. The `get_data.py` is used for this (one per page - 291796 pages in total)
2. The `dask` library is used to avoid kernel crashes and preprocess the data to have several coherent DataFrames with the relevant information.
3. For ease of use and efficiency, the data is now stored in a sqlite database
4. Creation of Visualizations by querying the Database and API

> All visualizations are create purely with python and the `plotly` library.  The details are shown in the `analysis.ipynb` notebook. 

> **NOTE: The data was downloaded late November 2024. All considerations in this notebook are up to this point in time.**