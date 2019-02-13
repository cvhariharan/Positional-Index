import json

# Assuming that the json file has a key-value pair as "docslist" pointing to a list of all documents

class Processor:
    def __init__(self, path):
        self.indexPath = path
        f = open(path, "r")
        jsonString = f.read()
        # print(jsonString)
        self.index = json.loads(jsonString)
        self.documents = self.index["docslist"]

    def getPostingList(self, keyword):
        try:
            return self.index[keyword]
        except KeyError:
            print("No such keyword in the index: "+keyword)
            return []

    
    def andMerge(self, list1, list2):
        # Not necessary is already sorted
        list1.sort()
        list2.sort()

        output = []
        i = 0 #pointing to list1
        j = 0 #pointing to list2
        while i < len(list1) and j < len(list2):
            if int(list1[i]) < int(list2[j]):
                i += 1
            elif int(list1[i]) > int(list2[j]):
                j += 1
            else:
                output.append(list1[i])
                i += 1
                j += 1
        return output

    def orMerge(self, list1, list2):
        # Not necessary is already sorted
        list1.sort()
        list2.sort()
        
        output = []
        i = 0 #pointing to list1
        j = 0 #pointing to list2
        while i < len(list1) and j < len(list2):
            if int(list1[i]) < int(list2[j]):
                output.append(list1[i])
                i += 1
            elif int(list1[i]) > int(list2[j]):
                output.append(list2[j])
                j += 1
            else:
                output.append(list1[i])
                i += 1
                j += 1

        while i < len(list1):
            output.append(list1[i])
            i += 1
        
        while j < len(list2):
            output.append(list2[j])
            j += 1

        return output

    def diffMerge(self, list1, list2):
        # Outputs components in list1 but not in list2
        output = set(list1) - set(list2)
        output = list(output)
        output.sort()
        return output
    
    def notKeyword(self, keyword):
        output = self.getPostingList(keyword)
        output = self.diffMerge(self.documents, output)
        return output
    
    def andKeyword(self, keyword1, keyword2):
        postingList1 = self.getPostingList(keyword1)
        postingList2 = self.getPostingList(keyword2)
        return self.andMerge(postingList1, postingList2)
    
    def orKeyword(self, keyword1, keyword2):
        postingList1 = self.getPostingList(keyword1)
        postingList2 = self.getPostingList(keyword2)
        return self.orMerge(postingList1, postingList2)

    


            

