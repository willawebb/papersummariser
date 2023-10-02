# papersummariser
Simple program to get the summary on the latest computer vision preprints from arXiv.

This program can also retrieve images from within the PDF of the paper for further analysis.

Unfortunately OpenAI doesn't currently provide an image ingestion service that one could use
for image recognition and description; however, the utility is obvious and would be simple to
implement.

Thoughts on how to solve that:

As this little project stands, there's much more to do to make this more than a way to help scrape
images from a PDF on arXiv; that could be useful in other areas, but especially for scientific papers
the insight you'll gain from figures would be better if there was some way to process them.

Several papers exist using mixed OCR/deep learning techniques meant to read graphs and create annotations for them:

https://openaccess.thecvf.com/content/WACV2021/papers/Luo_ChartOCR_Data_Extraction_From_Charts_Images_via_a_Deep_Hybrid_WACV_2021_paper.pdf
https://arxiv.org/ftp/arxiv/papers/1812/1812.10636.pdf

And there appear to be several implementations of this, with CVrane's ChartReader looking to be the most promising:

https://github.com/Cvrane/ChartReader

I understand this project was originally intended to be a very simple 1-3 hour project, and perhaps my choice to spend some of that time
just exploring the possibilities of Metaphor's technology has resulted in the original code being lackluster in terms of ability. As such,
I am going to choose to continue working on this, as I believe I'm capable of a fair bit more.