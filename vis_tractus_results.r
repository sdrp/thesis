# Visualize Tractus Results
library(ggplot2)
TractusResults <- read.table(file = 'output_file_experiment.tsv', sep = '\t', header = TRUE)
TractusResults$Expression.Level <- as.factor(TractusResults$Expression.Level)
TractusResults$Predicted.Expression.Level <- as.factor(TractusResults$Predicted.Expression.Level)
p <- ggplot(TractusResults, aes(x=Expression.Level, y=Expression.Value, color=Predicted.Expression.Level)) + 
    geom_jitter(position=position_jitter(0.2))
p + scale_color_brewer(palette="Dark2")



