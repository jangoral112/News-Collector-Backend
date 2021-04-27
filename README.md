# News Collector Backend

Backend side to News Collector application.

[tables_creation.sql](https://github.com/jangoral112/News-Collector-Backend/blob/main/tables_creation.sql) contains MySql script for creating tables used in project. To connect with database fill [db_connection_config.py](https://github.com/jangoral112/News-Collector-Backend/blob/main/src/db_connection_config.py)

[aws_lambdas](https://github.com/jangoral112/News-Collector-Backend/tree/main/aws_lambdas) contains AWS lambdas codes used with API Gatway to create endpionts.

[src](https://github.com/jangoral112/News-Collector-Backend/tree/main/src) contains business logic. Packed with [requirements](https://github.com/jangoral112/News-Collector-Backend/blob/main/requirements.txt) and uploaded to S3 can be used as a layer for lambdas.
