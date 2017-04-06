# Visualize Tractus Results
library(ggplot2)
TractusResults <- read.table(file = 'tract_dep_results.tsv', sep = '\t', header = TRUE)
TractusResults$Expression.Level <- as.factor(TractusResults$Expression.Level)
TractusResults$Predicted.Expression.Level <- as.factor(TractusResults$Predicted.Expression.Level)

# Set the plot mode to "jitter" - more aesthetically pleasing, less clear
p <- ggplot(TractusResults, aes(x=Expression.Level, y=Expression.Value, color=Predicted.Expression.Level)) + 
    geom_jitter(position=position_jitter(0.2))

# Set the plot mode to "dodge" - clear
#p <- ggplot(TractusResults, aes(x=Expression.Level, y=Expression.Value, color=Predicted.Expression.Level)) + 
#    geom_jitter(position=position_dodge(0.8))

# Change the color scheme
p + scale_color_brewer(palette="Dark2")



