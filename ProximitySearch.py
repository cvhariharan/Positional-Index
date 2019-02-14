import json

def getResults(query):
    results = set()
    
    f = open('./positional-index.json', "r")
    jsonString = f.read()    # print(jsonString)
    index = json.loads(jsonString)
    documents = index["docslist"]

    if "\\" in query:
        tokens = query.split('\\')
        i = 0
        first = True
        while i < (len(tokens) - 1):
            temp_set = set()
            p1 = tokens[i].strip()
            if tokens[i+1].isdigit():
                
                num = int(tokens[i+1])
                p2 = tokens[i+2].strip()
                try:
                    d1 = index[p1]
                    d2 = index[p2]
                except KeyError:
                    print("Please check the keywords...")
                    break
                i += 2
            
                for key in d1.keys():
                    if key in d2.keys():
                        l1 = d1[key]
                        l2 = d2[key]
                        for j in range(len(l1)):
                            for k in range(len(l2)):
                                if (l2[k] - l1[j]) == num:
                                    if first:
                                        results.add(key)
                                    else:
                                        temp_set.add(key)
                if not first:
                    results = results.intersection(temp_set)
                
            
            else:
                i += 1

            first = False
        
    else:
        return list(index[query].keys())
        
    return results

query = input()
print(getResults(query))