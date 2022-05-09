library(ggplot2)co

#Change the file to the location of where it lies.
argument.length.stats <- read.csv2("length_statistics.csv", sep = ",")
argument.count.stats <- read.csv2("count_statistics.csv", sep = ",")

#General structure of the data
ggplot(data = argument.count.stats, aes(x=Admissible.sets)) + geom_bar() + labs(x = "Admissible Sets")
ggplot(data = argument.count.stats, aes(x=factor(Complete.sets))) + geom_bar() + labs(x = "Complete Sets")
ggplot(data = argument.count.stats, aes(x=factor(Prefered.sets))) + geom_bar() + labs(x = "Preferred Sets")
ggplot(data = argument.count.stats, aes(x=factor(Stable.sets))) + geom_bar() + labs(x = "Stable Sets")

ggplot(data = argument.length.stats, aes(x=Set.length)) + geom_bar() + labs(x = "Length of Sets")

#Relations Figures
color_range <- colorRampPalette(c("blue", "green"))
my_colors <- color_range(20)
ggplot(data = argument.count.stats, aes(x=Arguments, y=Edges, color=Stable.sets)) + geom_point(position = "jitter")  + scale_colour_gradientn(colors = my_colors) + labs(color="Amount Stable Sets")
ggplot(data = argument.count.stats, aes(x=Arguments, y=Edges, color=Prefered.sets)) + geom_point(position = "jitter")  + scale_colour_gradientn(colors = my_colors) + labs(color="Amount Preferred Sets")
ggplot(data = argument.count.stats, aes(x=Arguments, y=Edges, color=Complete.sets)) + geom_point(position = "jitter")  + scale_colour_gradientn(colors = my_colors) + labs(color="Amount Complete Sets")
ggplot(data = argument.count.stats, aes(color=factor(Arguments), y=Edges, x=Admissible.sets)) + geom_point(position = "jitter") + labs(x="Amount Admissible Sets", color="Arguments")

#Length of extensions
argument.length.admissible <- subset(argument.length.stats, argument.length.stats$Type=="admissible")
argument.length.complete <- subset(argument.length.stats, argument.length.stats$Type=="complete")
argument.length.preferred <- subset(argument.length.stats, argument.length.stats$Type=="preferred")
argument.length.stable <- subset(argument.length.stats, argument.length.stats$Type=="stable")

#Length Figures
ggplot(data = argument.length.admissible, aes(x=Arguments, y=Edges, color=Set.length)) + geom_point(position = "jitter")  + scale_colour_gradientn(colors = my_colors) + labs(color="Length Admissible Sets")
ggplot(data = argument.length.complete, aes(x=Arguments, y=Edges, color=Set.length)) + geom_point(position = "jitter")  + scale_colour_gradientn(colors = my_colors) + labs(color="Length Complete Sets")
ggplot(data = argument.length.preferred, aes(x=Arguments, y=Edges, color=Set.length)) + geom_point(position = "jitter")  + scale_colour_gradientn(colors = my_colors) + labs(color="Length Preferred Sets")
ggplot(data = argument.length.stable, aes(x=Arguments, y=Edges, color=Set.length)) + geom_point(position = "jitter") + scale_colour_gradientn(colors = my_colors) + labs(color="Length Stable Sets")

#Hypothesis 1
cor(argument.count.stats$Edges, argument.count.stats$Admissible.sets, method = "pearson")
cor(argument.count.stats$Edges, argument.count.stats$Admissible.sets, method = "spearman")
ggplot(data = argument.count.stats, aes(x=Edges, y=Admissible.sets)) + geom_point(position = "jitter") + labs(y="Admissible sets")
cor(argument.count.stats$Edges, argument.count.stats$Arguments, method = "pearson")
cor(argument.count.stats$Edges, argument.count.stats$Arguments, method = "spearman")
cor(argument.count.stats$Arguments, argument.count.stats$Admissible.sets, method = "pearson")
cor(argument.count.stats$Arguments, argument.count.stats$Admissible.sets, method = "spearman")

#Hypothesis 2
cor(argument.length.preferred$Edges, argument.length.preferred$Set.length, method = "pearson")
cor(argument.length.preferred$Edges, argument.length.preferred$Set.length, method = "spearman")

#Hypothesis 3
cor(argument.count.stats$Arguments, argument.count.stats$Complete.sets, method = "pearson")
cor(argument.count.stats$Arguments, argument.count.stats$Complete.sets, method = "spearman")
