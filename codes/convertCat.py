def ConvertCat(dataset, catCol,numCol):
    """this function will binarize a dataset given in parametrer and return the dataset with categorical columns binarise by one-hot encoding"""
    encs={}
    X_train_1=dataset[catCol]
    X=dataset[numCol]
    catCol=X_train_1.columns
    for col in catCol:
        data=dataset[[col]]
        enc= LabelBinarizer()
        enc.fit(data)
        # Fitting One Hot Encoding on train data
        temp = enc.transform(dataset[[col]])
        # Changing the encoded features into a data frame with new column names
        temp=pd.DataFrame(temp,columns=enc.classes_)
        # In side by side concatenation index values should be same
        # Setting the index values similar to the X_train data frame
        temp=temp.set_index(dataset.index)
        # adding the new One Hot Encoded varibales to the train data frame
        
        X=pd.merge(temp,X,right_index=True,left_index=True)
        #saving the encoder into a dict for others operations
        encs[col]=enc
    return X,encs