#DATA 557 Project: Ice Cream Analysis

#=============================================================

#Question 10: Do common ice cream flavors have the same proportion of 5's?

#Open CSV file
data = read.csv(file.choose(), header=TRUE)
colnames(data)

#=============================================================
#Comparing proportions of 5's for chocolate, strawberry, and vanilla for all brands

#Subset dataframe
subset_cols = c('key', 'chocolate', 'strawberry', 'vanilla', 'stars')
subset_data = subset(data, select = subset_cols)
subset_data$is_5 = ifelse(subset_data$stars == 5, 1, 0)
subset_data

#Create new column to reconstruct dummy variable 
what_flavor = rep(NA, nrow(subset_data))

#For loop to get values for each observation
for (i in 1:nrow(subset_data)){
  if(subset_data$chocolate[i] == 1){
    what_flavor[i] = "chocolate"}
  else if(subset_data$strawberry[i] == 1){
    what_flavor[i] = "strawberry"}
  else if(subset_data$vanilla[i] == 1){
    what_flavor[i] = "vanilla"}
}

unique(what_flavor)

#add flavor column to df
subset_data = cbind(subset_data,what_flavor)
subset_data

#counts of 5's and not 5'sfor each flavor and whether 
subset_table = table(subset_data$what_flavor, subset_data$is_5)

#perform chi-square test
chisq.test(subset_data$what_flavor, subset_data$is_5, correct=FALSE)
#================================================

#Comparing chocolate, strawberry, and vanilla for each brand