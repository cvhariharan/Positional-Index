## Proximity Search
Run the positional indexer using  
```
python3 PositionalIndex.py
```
make sure that the dataset is in the same directory  
Next run the proximity search script  
```
python3 ProximitySearch.py
```
this will automatically try to locate positional-index.json in the same directory.  
Queries of the form  
```
keyword1\num2\keyword2\num2\keyword3  
```
supported  
For example
```
times\1\square
```

## Biword Search
Although positional index allows for biword searches, a separate biword index has been created.
Run  
```
python3 BiwordIndex.py
```
then  
```
python3 query_parser.py
```
queries with multiple AND/OR and phrases with utmost 2 words are supported.