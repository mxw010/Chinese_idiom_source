library(ggplot2)
library(showtext)
library(dplyr)
library(gridExtra)
library(grid)

showtext_auto()
x <- read.csv("sourced.csv")
temp <- table(x$book)


#top 30 for plotting
candidate <-  names(sort(temp,decreasing=T)[1:30])
df <- x %>% group_by(book) %>% mutate(count_name = n())

png("idiom.png", height=1500,width=750)
plot1 <- ggplot(data=subset(df, book %in% candidate), aes(x=reorder(book, count_name))) +
  geom_bar(stat="count") + 
  xlab("来源") + 
  ylab("词量") + 
  theme_bw() +
  theme(axis.text = element_text(size=20), 
        axis.title = element_text(size=25))  +
  coord_flip()
  
df1 <- subset(x, book == "史记") %>% group_by(chapter) %>% mutate(count_name = n()) 
plot2 <- ggplot(data=subset(df1, count_name > 10),aes(x=reorder(chapter, count_name)))+
  geom_bar(stat="count") + 
  xlab("史记·卷") + 
  ylab("词量") + 
  theme_bw() +
  theme(axis.text = element_text(size=20), 
        axis.title = element_text(size=25)) +
  coord_flip() +
  annotate("text", x = 0, y = 50, label = "https://github.com/mxw010/Chinese_idiom_source",
           hjust=1.1, vjust=-1.1, col="black", cex=6, alpha=0.8,
           fontface = "bold")
grid.arrange(plot1, plot2, ncol=1, nrow=2, top = textGrob("成语源自何处？", gp=gpar(fontsize=36,font=3)))
dev.off()
