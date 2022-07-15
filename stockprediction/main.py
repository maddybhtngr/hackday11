import mysql.connector
import uuid
import threading
import time
import trend_predictor
import buzz_predictor

mydb = mysql.connector.connect(
    host="localhost",
    user="bhatnagar.madhur",
    password="1234",
    database="hackday"
)
mycursor = mydb.cursor()


def ingest_stock(stock):
    # TODO - check if valid stock
    # TODO - check if stock has already been processed for the day

    # ingest the stock and return the request ID
    request_id = str(uuid.uuid4())

    mycursor.execute("SELECT stock_name, prediction FROM ingestion_table where status='finalized' and stock_name='{0}'".format(stock))
    result = mycursor.fetchall()

    if not result:
        sql = "insert into ingestion_table (request_id, stock_name, prediction, status) values(%s, %s, null, 'ingested')"
        val = (request_id, stock)
        mycursor.execute(sql, val)
        mydb.commit()
    else:
        print(result)
        return result


def orchestrate():
    while True:
        time.sleep(5)
        mycursor.execute("SELECT stock_name FROM ingestion_table where status='ingested'")
        myresult = mycursor.fetchall()

        stocks = set()

        for x in myresult:
            stocks.add(x[0])

        for stock in stocks:
            prediction = handler(stock)
            sql = "UPDATE ingestion_table SET status = 'finalized', prediction = '{1}' WHERE stock_name = '{0}' ".format(stock, prediction)
            mycursor.execute(sql)
            mydb.commit()
            print("Data is ready")


def handler(stock):
    trend_prediction = trend_predictor.get_prediction(stock)
    buzz_prediction = buzz_predictor.get_prediction(stock)
    return trend_prediction + buzz_prediction


ingest_stock('M&M')
orchestrator_thread = threading.Thread(target=orchestrate)
orchestrator_thread.start()
