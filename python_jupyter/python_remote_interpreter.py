import pandas as pd
import platform

if __name__ == '__main__':
    df = pd.DataFrame({'col1': [1.0] * 5,
                       'col2': [2.0] * 5,
                       'col3': [3.0] * 5}, index=range(1, 6), )
    df2 = pd.DataFrame({'col1': [10.0] * 5,
                        'col2': [100.0] * 5,
                        'col3': [1000.0] * 5}, index=range(1, 6), )
    df3 = pd.DataFrame({'col1': [0.1] * 5}, index=range(1, 6), )

    x = pd.DataFrame(df.values * df2.values, columns=df.columns, index=df.index)

    print(x)
    print(platform.system())
    print(platform.release())
    import sys

    print(sys.version)
    print(sys.path)
    sys.path += [
        '',
        '/tmp/spark-f230ccdb-73d3-4a3a-a76a-5282ea48190b/userFiles-a54890a7-76c3-42e7-85d6-c6b97a291a54',
        '/usr/local/spark/python',
        '/usr/local/spark/python/lib/py4j-0.10.7-src.zip',
        '/opt/conda/lib/python36.zip', '/opt/conda/lib/python3.6',
        '/opt/conda/lib/python3.6/lib-dynload',
        '/opt/conda/lib/python3.6/site-packages',
        '/opt/conda/lib/python3.6/site-packages/IPython/extensions',
        '/home/jovyan/.ipython'
    ]

    from pyspark import SparkContext

    from pyspark import SparkContext  # And then try to import SparkContext.

    sc = SparkContext.getOrCreate()
    log4jLogger = sc._jvm.org.apache.log4j
    LOGGER = log4jLogger.LogManager.getLogger(__name__)

    words = sc.parallelize(["scala", "java", "python", "spark"])
    counts = words.count()
    print("How many words? {}".format(str(counts)))


    def prepare_row(row):
        """
        Converts a row into an object with the product id as key. the key is an identifier for an experiment.
        :param row: A list of [variation, is_control, metric_value, n_total] for each experiments
        :return: A tuple: (experiment_fingerprint, [[variation], [is_control], [metric_value], [n_total]])
        """

        experiment_fingerprint = row['key']
        is_control = row['is_control']
        n_total = row['tot']

        return experiment_fingerprint, [[is_control], [n_total]]


    def reducer_function(row1, row2):
        """
        Reduce two rows to one tuple. Expects rows of the form ([variation], [is_control], [metric_value], [n_total])
        :return: A tuple of the form ([variation], [is_control], [metric_value], [n_total])
        """

        # run model
        # xgboost()
        return row1[0] + row2[0], row1[1] + row2[1]


    x = {'key': 1, 'is_control': 'yes', 'tot': 200}
    y = {'key': 2, 'is_control': 'no', 'tot': 400}
    z = {'key': 1, 'is_control': 'yes', 'tot': 1000}
    data = [x, y, z]
    my_rdd = sc.parallelize(data)
    parsed_data = my_rdd.map(prepare_row).reduceByKey(reducer_function).collect()
    print(parsed_data)
