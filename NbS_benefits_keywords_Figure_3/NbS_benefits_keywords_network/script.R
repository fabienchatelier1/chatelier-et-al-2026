library(readr)


savedrecs_4_ <- read_excel("C:/Users/fabien/Desktop/updated database/NbS benefits_5635/savedrecs (4).xls")
savedrecs_5_ <- read_excel("C:/Users/fabien/Desktop/updated database/NbS benefits_5635/savedrecs (5).xls")
savedrecs_6_ <- read_excel("C:/Users/fabien/Desktop/updated database/NbS benefits_5635/savedrecs (6).xls")
savedrecs_7_ <- read_excel("C:/Users/fabien/Desktop/updated database/NbS benefits_5635/savedrecs (6).xls")
savedrecs_8_ <- read_excel("C:/Users/fabien/Desktop/updated database/NbS benefits_5635/savedrecs (8).xls")
savedrecs_9_ <- read_excel("C:/Users/fabien/Desktop/updated database/NbS benefits_5635/savedrecs (9).xls")

nbs_benefits = rbind(savedrecs_4_,savedrecs_5_,savedrecs_6_, savedrecs_7_, savedrecs_8_, savedrecs_9_)

nbs_benefits_reduced= data.frame(nbs_benefits$`Article Title`,nbs_benefits$Abstract)
colnames(nbs_benefits_reduced)= c("TI","AB")
write.csv(nbs_benefits_reduced, file="nbs_benefits_reduced.csv",row.names = FALSE)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

words_selections <- read_csv("C:/Users/fabien/Desktop/nbs network/words selections.csv")
words_selections_reduced = subset(words_selections, words_selections$...2 =="y")
colnames(words_selections_reduced) = c("Label","To_keep")


nodes <- read_csv("C:/Users/fabien/Desktop/data.csv")
nodes_reduced = data.frame(nodes$id, nodes$label)
colnames(nodes_reduced) = c("Id","Label")
edges <- read_csv("C:/Users/fabien/Desktop/data2.csv")
colnames(edges)= c("Source","Target","weight")

nodes_to_keep = merge(x=nodes_reduced, y= words_selections_reduced, by.x = "Label",by.y ="Label")
nodes_to_keep = data.frame(nodes_to_keep$Id,nodes_to_keep$Label)
colnames(nodes_to_keep) = c("Id","Label")

edges_num_1 = merge(x=edges, y=nodes_to_keep, by.x = "Source", by.y = "Id"  )
edges_num_1 = data.frame(edges_num_1$Label, edges_num_1$Source, edges_num_1$Target,edges_num_1$weight)
colnames(edges_num_1) = c("Source","Source_num","Target_num","weight")
edges_num_2 = merge(x= edges_num_1, y = nodes_to_keep, by.x = "Target_num",by.y ="Id")
edges_num_2 = data.frame(edges_num_2$Source, edges_num_2$Label, edges_num_2$Source_num, edges_num_2$Target_num,edges_num_2$weight )
colnames(edges_num_2) = c("source","target","source_num","target_num","weight")

edges_num_3 = data.frame(edges_num_2$source_num, edges_num_2$target_num, edges_num_2$weight)
colnames(edges_num_3)= c("source","target","weight")

#export

write.csv(edges_num_3, file= "edges.csv",row.names=FALSE)
write.csv(nodes_to_keep, file= "nodes.csv",row.names=FALSE)