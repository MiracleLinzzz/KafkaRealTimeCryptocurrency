set ZOOKEEPER_LOGS_PATH=C:\tmp\zookeeper
set KAFKA_LOGS_PATH=C:\tmp\kafka-logs
set KAFKA_PATH=F:\kafka\kafka_2.12-3.1.0
set ANACONDA_PATH=F:\anaconda3\envs\stream
set THIS_PATH=C:\Users\81051\Desktop\code

@REM echo Preparing system
@REM echo off    
@REM rmdir /q /s %ZOOKEEPER_LOGS_PATH%
@REM rmdir /q /s %KAFKA_LOGS_PATH%
@REM timeout 1
@REM echo Starting Zookeeper
@REM start cmd /k %KAFKA_PATH%\bin\windows\zookeeper-server-start.bat %KAFKA_PATH%\config\zookeeper.properties
@REM timeout 5
@REM echo Starting Kafka Server
@REM start cmd /k %KAFKA_PATH%\bin\windows\kafka-server-start.bat %KAFKA_PATH%\config\server.properties
@REM timeout 5
@REM echo Starting Kafka Producer
@REM start cmd /k %ANACONDA_PATH%/python.exe %THIS_PATH%/src/kafka/realTimeDataCollector.py 
@REM timeout 1
@REM echo Starting Spark as Consumer
@REM start cmd /k %ANACONDA_PATH%/python.exe %THIS_PATH%/src/eval.py /src/data/train.csv --model-name model_double-dqn_GOOG_50 --debug  

echo Starting web server
start cmd /k %ANACONDA_PATH%/python.exe %THIS_PATH%/server/manage.py runserver 