# Plot Results of Length Tests

library(ggplot2)
LenResults <- read.table(file = 'len_test_scaled.tsv', sep = '\t', header = TRUE)
g <- ggplot(data=LenResults,
       aes(x=Haplotype_Length, y=False_Classification_Proportion)) +
        geom_line(color='chartreuse3', size=0.75)

# Set y scale 
g <- g + scale_y_continuous(limits=c(0,1), breaks=seq(0,1,0.1))

# Set the title
g <- g + labs(title = "Common Tract Size: Scaled")#, subtitle=expression(italic(n)~"= 100"))
g <- g + theme(plot.title = element_text(size=15, hjust = 0.5, face="bold", 
                                         margin = margin(10, 0, 10, 0)))#,
               #plot.subtitle = element_text(size = 10, hjust = 0.5))

# Set the axes
g <- g+labs(x="Haplotype Length", y= "False Classification Proportion")
g <- g + theme(
  axis.title.x = element_text(color="black", vjust=0.35),
  axis.title.y = element_text(color="black" , vjust=0.35)   
)

# Change the color scheme
g + scale_color_brewer(palette="Dark2")