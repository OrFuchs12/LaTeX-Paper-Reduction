import arxiv

client = arxiv.Client()

# Search for the 10 most recent articles matching the keyword "quantum."
search = arxiv.Search(
  query = "AAAI",
  sort_by = arxiv.SortCriterion.SubmittedDate
)

results = client.results(search)

for r in client.results(search):
  title= r.title
  words = title.split()[:3]
  result = ' '.join(words)
  
  if 'AAAI' in r.comment:
    r.download_source(dirpath="C:/Users/micha/OneDrive/שולחן העבודה/LaTeX-Paper-Reduction/new_papers_creation/tar_files", filename=f"{result}.tar.gz")