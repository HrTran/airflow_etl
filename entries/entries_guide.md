# Config DAG entries

The DAG entries is the config specific for each DAG

## Structure
The entry file is composed of:
* input
* transformations
* output
* isDisable

where: 
- `input` contains multiple data sources configuration, and define columns should be extracted.
- `transformation` contains transform operators based on extracted columns.
- `output` contains target data sources which will be written to.
- `isDisable` is used for disable the DAG

## Details
* Input:  
  |_ `type`: data source type. E.g: Kafka, Postgres, MySQL, ...  
  |_ `table`: table name (if data source type is Postgres or MySQL)  
  |_ `db`: the connection name on Airflow  
  |_ `select`: define which fields will be extracted. Can be list of field names,
             cast to specific type, or apply operators on it.
* Output:  
  |_ `type`: data source type. E.g: Kafka, Postgres, MySQL, ...  
  |_ `table`: table name (if data source type is Postgres or MySQL)  
  |_ `write_mode`: append, replace  
  |_ `partition`: define fields which are partitioned  
  |_ `index`: define fields which are indexed.
* Tranformation: contains multiple items which has  
  |_ `table`: the table which is defined in `Input` section
  |_ `operations`: transform operations on the pandas DataFrame using eval()
* isDisable: just true or false. Specify whether the DAG runs or not.

## Examples
```json
{
	"input": [
		{
			"type": "postgres",
            "table": "source_A",
			"db": "alpha",
			"select": [
				{
					"fields": ["id", "a", "b", "c"]
				},
				{
					"fields": "d",
					"type": "string"
				},
				{
					"fields": "e",
					"type": "string",
					"operator": "SUBSTR",
					"params": "3"
				}
			]
		},
		{
            "type": "postgres",
			"table": "source_B",
			"db": "alpha",
			"select": [
				{
					"fields": ["id", "a", "b", "c"]
				}
			]
		}
	],
	"transformation": [
      {
        "table": "source_B",
        "operations": ["d = a + b", "e = b + d"]
      }
	],
	"output": [
		{
			"type": "postgres",
			"table": "target_C",
			"write_mode": "append"
		}
	],
	"isDisable": false
}
```