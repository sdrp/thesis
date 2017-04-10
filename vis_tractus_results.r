# Visualize Tractus Results
library(ggplot2)
TractusResults <- read.table(file = 'random_output.tsv', sep = '\t', header = TRUE)
TractusResults$Expression.Level <- as.factor(TractusResults$Expression.Level)
TractusResults$Prediction <- as.factor(TractusResults$Prediction)

# Set the plot mode to "jitter" - more aesthetically pleasing, less clear
g <- ggplot(TractusResults, aes(x=Expression.Level, y=Expression.Value, color=Prediction)) + 
    geom_jitter(position=position_jitter(0.2))

# Set the plot mode to "dodge" - clear
#p <- ggplot(TractusResults, aes(x=Expression.Level, y=Expression.Value, color=Predicted.Expression.Level)) + 
#    geom_jitter(position=position_dodge(0.8))

# Set the title
g <- g + ggtitle(expression(atop("Random Expression", italic(n)~"= 100   "~italic(p) ~ "=100")))
g <- g + theme(plot.title = element_text(size=15, face="bold", 
                                  margin = margin(10, 0, 10, 0)))

# Set the axes
g <- g+labs(x="Expression Level", y= "Expression Value (RPKM)")
g <- g + theme(
  axis.title.x = element_text(color="black", vjust=0.35),
  axis.title.y = element_text(color="black" , vjust=0.35)   
)


# Change the color scheme
g + scale_color_brewer(palette="Dark2")



