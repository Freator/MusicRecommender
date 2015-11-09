from __future__ import print_function

from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
from pyspark import SparkContext, SparkConf
from src.parser import parse_line
import os
import argparse


def main():

    parser = argparse.ArgumentParser(description='Create a collaborative filtering system for music ratings.')
    parser.add_argument('datafile', type=str, nargs=1,
                        help='absolute path to the file you wish use for testing/training')

    args = parser.parse_args()
    path = args.datafile[0]
    dataFile = 'file:///{}'.format(path)
    print("dataFile = ", dataFile)

    collaborative_filter(dataFile)


def collaborative_filter(dataFile):

    conf = SparkConf() \
        .setAppName("Collaborative Filter") \
        .set("spark.executor.memory", "5g")
    sc = SparkContext(conf=conf)
    # Load and parse the data
    data = sc.textFile(dataFile)
    ratings_map = data.map(parse_line)
    count = ratings_map.count()
    print("The count is: ", count)
    ratings = ratings_map.map(lambda entry: Rating(entry['user']['hash'],
                                                   entry['song']['hash'],
                                                   entry['rating']))
    # #ratings = data.map(lambda l: l.split()).map(lambda l: Rating(int(l[0]), int(l[1]), float(l[2])))
    #
    # # Build the recommendation model using Alternating Least Squares
    rank = 10
    numIterations = 10
    model = ALS.train(ratings, rank, numIterations)
    # # Evaluate the model on training data
    # testdata = ratings.map(lambda p: (p[0], p[1]))
    # predictions = model.predictAll(testdata).map(lambda r: ((r[0], r[1]), r[2]))
    # ratesAndPreds = ratings.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
    # MSE = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
    # print("Mean Squared Error = " + str(MSE))
    #
    # # Save and load model
    # path = os.path.dirname(os.path.realpath(__file__))
    # path = 'file:///' + path + '/myModelPath'
    # print(50*'*')
    # print('The path is: ' + path)
    # print(50*'*')
    # model.save(sc, path)
    # sameModel = MatrixFactorizationModel.load(sc, path)


if __name__ == '__main__':
    main()