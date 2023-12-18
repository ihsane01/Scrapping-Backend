from flask import Flask
from flask_cors import CORS

from pyspark.sql import SparkSession
from collections import Counter
from flask import json
from flask import jsonify
from pyspark import SparkContext
import pyspark
from pyspark.sql import SQLContext 


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


spark = SparkSession.builder.appName("myApp") \
.config("spark.mongodb.input.uri",
"mongodb://127.0.0.1/datajournals.data") \
.config("spark.mongodb.output.uri",
"mongodb://127.0.0.1/datajournals.data") \
.config('spark.jars.packages',
'org.mongodb.spark:mongo-spark-connector_2.12:2.4.2') \
.getOrCreate()

# df = spark.read.format("mongo").load()
# df.show()

sqlC = SQLContext(spark)
# python -m flask run
 
@app.route('/api/topjournals/')
def topjournals():
    df = spark.read.format("mongo").load()
    pandas_df = df.groupBy("Publisher").count().sort("count",ascending=True).toPandas().tail(7)
    return pandas_df.to_json(orient='records').replace('count','value').replace('journal','name')


@app.route('/api/collaborationc/')
def getCountriesCol():
    df = spark.read.format("mongo").load()
    pandas_df = df.groupBy("countries").count().sort("count", ascending=True).toPandas()
    pandas_df = pandas_df[pandas_df['countries'].str.contains(";")]
    vocab = Counter()
    for index, row in pandas_df.iterrows():
        a = row['countries'].strip().replace('; ', ';')
        sorted_words = ';'.join(a.lower().split(";"))
        vocab[sorted_words] += int(row['count'])
    result = [{'name': key, 'value': value} for key, value in vocab.items()]
    return jsonify(result)


@app.route('/api/year/')
def meteo():
    df = spark.read.format("mongo").load()
    pandas_df = df.groupBy("Year").count().sort("count", ascending=True).toPandas()
    return pandas_df.to_json(orient='records').replace('count','value').replace('Year', 'name')


@app.route('/api/countries/')
def pubContr():
    df = spark.read.format("mongo").load()
    pandas_df = df.groupBy("countries").count().sort(  "count", ascending=True).toPandas()
    pandas_df = pandas_df[~pandas_df['countries'].str.contains(";")]
    return pandas_df.to_json(orient='records').replace('count','value').replace('valueries', 'name')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    # app.listen(str,(error)=>{if(error) console.log(error) })