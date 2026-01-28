library(networkD3)
library(readxl)

# Load data
df <- read_excel("arrive by region.xlsx")

# Convert column names to character type
names(df) <- as.character(names(df))

# Prepare data for the Sankey diagram
nodes <- unique(c(df$`Arrivals from regions`, df$Country, 'Fiji', 'French Polynesia', 'Samoa'))
nodes <- data.frame(name = nodes)

# Create source and target indices
df$source <- match(df$`Arrivals from regions`, nodes$name) - 1
df$target <- match(df$Country, nodes$name) - 1

# Create links data frame
links <- data.frame(
  source = df$source,
  target = df$target,
  value = df$`2019`
)

# Generate Sankey diagram
sankey <- sankeyNetwork(
  Links = links,
  Nodes = nodes,
  Source = "source",
  Target = "target",
  Value = "value",
  NodeID = "name",
  units = "number of arrivals",
  fontSize = 16,
  nodeWidth = 30
)

# Save Sankey diagram as HTML file
#saveNetwork(sankey, file = "sankey_diagram.html")
sankey
