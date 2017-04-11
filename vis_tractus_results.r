# Visualize Tractus Results
library(ggplot2)
TractusResults <- read.table(file = 'kcnj12_method2.tsv', sep = '\t', header = TRUE)
TractusResults$Expression.Level <- as.factor(TractusResults$Expression.Level)
TractusResults$Prediction <- as.factor(TractusResults$Prediction)

# Set the plot mode to "jitter" - more aesthetically pleasing, less clear
g <- ggplot(TractusResults, aes(x=Expression.Level, y=Expression.Value, color=Prediction)) + 
    geom_jitter(position=position_jitter(0.2))

# Set the title
g <- g + labs(title = "Real Data: KCNJ12 Expression", subtitle=expression(atop("False Classification Proportion = 0.43", italic(n)~"= 14   "~italic(p) ~ "= 42")))
g <- g + theme(plot.title = element_text(size=15, hjust = 0.5, face="bold", 
                                  margin = margin(10, 0, 10, 0)),
               plot.subtitle = element_text(size = 10, hjust = 0.5))

# Set the axes
g <- g+labs(x="Expression Level", y= "Expression Value (RPKM)")
g <- g + theme(
  axis.title.x = element_text(color="black", vjust=0.35),
  axis.title.y = element_text(color="black" , vjust=0.35)   
)


# Change the color scheme
g + scale_color_brewer(palette="Dark2")



