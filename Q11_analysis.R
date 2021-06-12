#DATA 557 Project: Ice Cream Analysis

#=============================================================

#Question 11: Logistic Regression

#Open CSV file
data = read.csv(file.choose(), header=TRUE)
colnames(data)

#Subset data with dummies and ratings
subset_data = data[c(1:21674),c(8,17:111)]
colnames(subset_data)

#remove name column
subset_data = subset(subset_data, select = -c(name))

#=============================================================

#Missingness plot
  #Missing data have have a big impact on modeling
  #Horizontal lines indicate missing data for an instance, 
    #vertical blocks represent missing data for an attribute.
library(Amelia)
library(mlbench)
missmap(subset_data, col=c("blue", "red"), legend=FALSE)

#=============================================================

#Correlation matrix
#library(corrplot)
correlations = cor(subset_data[,2:95])
round(correlations,2)
#corrplot(correlations, method="circle")

#=============================================================

#Logistic regression
#Column for is_5
subset_data$is_5 = ifelse(subset_data$stars == 5, 1, 0)

#bananas, almonds, organic
model_1 = glm(is_5 ~ banana + contains_almonds + contains_organic, data = subset_data, family = binomial)
summary(model_1)

#Confidence intervals of model_1
confint(model_1)

#Wald test to see if predictors contribute to model
library(aod)
#banana
wald.test(b = coef(model_1), Sigma = vcov(model_1), Terms = 2)

#almond
wald.test(b = coef(model_1), Sigma = vcov(model_1), Terms = 3)

#organic
wald.test(b = coef(model_1), Sigma = vcov(model_1), Terms = 4)
