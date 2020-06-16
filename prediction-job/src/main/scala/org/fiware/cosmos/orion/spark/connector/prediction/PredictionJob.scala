package org.fiware.cosmos.orion.spark.connector.prediction

import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.fiware.cosmos.orion.spark.connector.{ContentType, HTTPMethod, OrionReceiver, OrionSink, OrionSinkObject}
import org.apache.spark.ml.feature.{VectorAssembler}
import org.apache.spark.ml.regression.{RandomForestRegressionModel}
import org.apache.spark.sql.SparkSession


/**
  * Prediction Job
  * @author @sonsoleslp
  */

case class PredictionResponse(socketId: String, predictionId: String, predictionValue: Int,
time: Int,day: Int,month: Int,year: Int,weekDay: Int) {
  override def toString :String = s"""{
  "socketId": { "value": "${socketId}", "type": "String"},
  "predictionId": { "value":"${predictionId}", "type": "String"},
  "predictionValue": { "value":${predictionValue}, "type": "Integer"},
time: Int,day: Int,month: Int,year: Int,weekDay: Int  }""".trim()
}
case class PredictionRequest(socketId: String, predictionId: String,
time: Int,day: Int,month: Int,year: Int,weekDay: Int)

object PredictionJob {
  final val URL_CB = "http://orion:1026/v2/entities/ResTicketPrediction1/attrs"
  final val CONTENT_TYPE = ContentType.JSON
  final val METHOD = HTTPMethod.PATCH
  final val BASE_PATH = "./prediction-job"

  def main(args: Array[String]): Unit = {
    val spark = SparkSession
      .builder
      .appName("PredictionJob")
      .master("local[*]")
      .getOrCreate()
    import spark.implicits._
    spark.sparkContext.setLogLevel("WARN")

    val ssc = new StreamingContext(spark.sparkContext, Seconds(1))
    // ssc.checkpoint("./output")

    // Load the numeric vector assembler
    //    val vectorAssemblerPath = "%s/models/numeric_vector_assembler.bin".format(BASE_PATH)
    //    val vectorAssembler = VectorAssembler.load(vectorAssemblerPath)
    val vectorAssembler = new VectorAssembler()
      .setInputCols(Array(
time: Int,day: Int,month: Int,year: Int,weekDay: Int      ))
      .setOutputCol("features")

    // Load model
    // val randomForestModelPath = "%s/models/spark_random_forest_classifier.flight_delays.5.0.bin".format(BASE_PATH)
    val model = RandomForestRegressionModel.load(BASE_PATH+"/model")

    // Create Orion Source. Receive notifications on port 9001
    val eventStream = ssc.receiverStream(new OrionReceiver(9001))

    // Process event stream to get updated entities
    val processedDataStream = eventStream
      .flatMap(event => event.entities)
      .map(ent => {
time: Int,day: Int,month: Int,year: Int,weekDay: Int        val socketId = ent.attrs("socketId").value.toString
        val predictionId = ent.attrs("predictionId").value.toString
        PredictionRequest(socketId, predictionId,
time: Int,day: Int,month: Int,year: Int,weekDay: Int        )
      })

    // Feed each entity into the prediction model
    val predictionDataStream = processedDataStream
      .transform(rdd => {
        val df = rdd.toDF
        val vectorizedFeatures  = vectorAssembler
          .setHandleInvalid("keep")
          .transform(df)
        val predictions = model
          .transform(vectorizedFeatures)
          .select("socketId","predictionId", "prediction", "year", "month", "day", "time")

        predictions.toJavaRDD
    })
      .map(pred=> PredictionResponse(pred.get(0).toString,
        pred.get(1).toString,
        pred.get(2).toString.toFloat.round,
pred.get(").toString.toInt,pred.get([).toString.toInt,pred.get(u).toString.toInt,pred.get(').toString.toInt,pred.get(t).toString.toInt,pred.get(i).toString.toNone,pred.get(m).toString.toNone,pred.get(e).toString.toNone,pred.get(').toString.toNone,pred.get(,).toString.toNone,pred.get( ).toString.toNone,pred.get(u).toString.toNone,pred.get(').toString.toNone,pred.get(d).toString.toNone,pred.get(a).toString.toNone,pred.get(y).toString.toNone,pred.get(').toString.toNone,pred.get(,).toString.toNone,pred.get( ).toString.toNone,pred.get(u).toString.toNone,pred.get(').toString.toNone,pred.get(m).toString.toNone,pred.get(o).toString.toNone,pred.get(n).toString.toNone,pred.get(t).toString.toNone,pred.get(h).toString.toNone,pred.get(').toString.toNone,pred.get(,).toString.toNone,pred.get( ).toString.toNone,pred.get(u).toString.toNone,pred.get(').toString.toNone,pred.get(y).toString.toNone,pred.get(e).toString.toNone,pred.get(a).toString.toNone,pred.get(r).toString.toNone,pred.get(').toString.toNone,pred.get(,).toString.toNone,pred.get( ).toString.toNone,pred.get(u).toString.toNone,pred.get(').toString.toNone,pred.get(w).toString.toNone,pred.get(e).toString.toNone,pred.get(e).toString.toNone,pred.get(k).toString.toNone,pred.get(D).toString.toNone,pred.get(a).toString.toNone,pred.get(y).toString.toNone,pred.get(').toString.toNone,pred.get(]).toString.toNone,pred.get(").toString.toNone    )

    // Convert the output to an OrionSinkObject and send to Context Broker
    val sinkDataStream = predictionDataStream
      .map(res => OrionSinkObject(res.toString, URL_CB, CONTENT_TYPE, METHOD))

    // Add Orion Sink
    OrionSink.addSink(sinkDataStream)
    sinkDataStream.print()
    predictionDataStream.print()
    ssc.start()
    ssc.awaitTermination()
  }
}
