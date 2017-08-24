class ChiSquareCalc(object):
    """this class is designed to calculated and interpret the relationship between 2 categorials variables by computing the chi square test between them
    you can find more on chi square test on this video https://www.youtube.com/watch?v=misMgRRV3jQ
    it will use pandas , numpy ,searborn matplotlib , scipy
    """
    def __init__(self, X,Y,dataset,**kwargs):
        """we will initailise the with 2 colums of a datafrme the input must be a data and columns names"""
        if isinstance(dataset,pd.DataFrame) and isinstance(X,str)and isinstance(Y,str) and X in dataset.columns and Y in dataset.columns :
            if operator.and_(operator.__eq__(dataset[X].dtypes, 'object'),operator.__eq__(dataset[Y].dtypes, 'object')):
                self.dataset=dataset
                self.X=dataset[X]
                self.Y=dataset[Y]
                self.contingency=pd.DataFrame()
                self.c=0
                self.p=0
                self.dof=0
                self.q=0.95 #lower tail probability
            else:
                raise TypeError('Class only deal wih categorial columns')
        else:
            raise TypeError('Columns names must be string and data must be a DataFrame')
    def contengencyTable(self):
        """this method will return a contengency table of the 2 variables"""
        self.contingency = pd.crosstab(self.X,self.Y)
        return self.contingency
    def chisquare(self):
        """this one will calculate the chi square value and return
        q: chi square results
        df: degree of freedom
        p: probability
        expexcted: excepected frequency table
        """
        if (not self.contingency.empty):
            self.c, self.p, self.dof, expected = chi2_contingency(self.contingency)
            return pd.DataFrame(expected,columns=self.contingency.columns,index=self.contingency.index)
        else:
            raise ValueError('contingency table must be initialised')
    def conclude(self,on):
        """
        we can decide to conclude on chi square value(chi) or on p (p)value
        Here is how we build the conclusion according to p value
         Probability of 0: It indicates that both categorical variable are dependent
         Probability of 1: It shows that both variables are independent.
         Probability less than 0.05: It indicates that the relationship between the variables is significant at 95% confidence
        And according to chi square value and df we use a ccritical value calculate with :
        q:lower tail probability
        df:degree of freedom
         the conclusion is approving or rejecting a null hypothesis
        """
        NulHyp='is no relationship between '+self.X+'and '+self.Y
        criticalValue=scs.chi2.ppf(q = self.q, df =self.dof)
        if on not in ['chi','p']:
            raise ValueError('choose chi or p')
        else:
            if on=='chi':
                if criticalValue > self.c:
                    return 'Accepted : '+NulHyp
                else:
                    return 'null hypothesis is rejected : '+NulHyp
            else:
                if self.p==0:
                    return ' It indicates that both categorical variable are dependent'
                elif self.p==1:
                    return 'It shows that both variables are independent'
                elif self.p <(1-self.q):
                    return 'It indicates that the relationship between the variables is significant at confidence of %s',self.q
                else:
                    return 'there is no relationship '
    def DrawPlot(self):
        """ and as for bonus you can draw plot to visualise the relationship """
        sns.countplot(hue=self.X,y=self.Y,data=self.dataset)
