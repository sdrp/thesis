# Noise Experiment Visualization
library("ggplot2")
NoiseResults <- read.table(file = 'noise_exp_results', sep = '\t', header = TRUE)
#NoiseResults$Num_Levels <- as.factor(TractusResults$Num_Levels)

g <- ggplot(data=NoiseResults,
       aes(x=Noise, y=False_Classification_Rate, colour=Num_Levels)) +
  geom_line(size=0.75)

# Set the title
g <- g + labs(title = "  Noise vs. False Classification", subtitle=expression(italic(n)~"= 100   "~italic(p) ~ "= 100"))
g <- g + theme(plot.title = element_text(size=15, hjust = 0.5, face="bold", 
                                         margin = margin(10, 0, 10, 0)),
               plot.subtitle = element_text(size = 10, hjust = 0.5),
               legend.title = element_blank())

# Set the axes
g <- g+labs(x="Noise", y= "False Classification Proportion")
g <- g + theme(
  axis.title.x = element_text(color="black", vjust=0.35),
  axis.title.y = element_text(color="black" , vjust=0.35)   
)

# Change the color scheme
g + scale_color_brewer(palette="Dark2")