# Connect to Data

There are several options for accessing data in your Record Bin deployment

## API Access

Call the endpoints and consume the Json Data directly:

```bash
curl -H "Content-Type: application/json" \
     --request POST \
     --data '{"username":"xyz","result":0, "action": "deleted"}' \
     "http://api.recordbin.co/api/v1/records/?apptoken=<token>
```

## Database Access

Connect directly to your database service.

#### Tableau Note

Jsaon field it's unusual to access:

```SQL
SELECT
  id,
  created_on,
  data,
  data::json->>'username' as username,
  data::json->>'result' as result
FROM records_record
```

## Tableau Web Connector

Create a Web Connector datasource and point it to `http://api.recordbin.com/connector/`.
You can use [this simmulator](http://tableau.github.io/webdataconnector/Simulator/) to ensure the connector is working properly.

### Accessing Data

To access a json field, create calculated fields using regex expressions:

#### Text Value

```
data = {"username":"Gui"}
>>> REGEXP_EXTRACT([Data],'"username":"((\\"|[^"])*)"')
Gui
```

#### Number Value

```
data = {"result":1}
>>> REGEXP_EXTRACT([Data],'"result":((\\"|[^"!,])*)')
1
```
