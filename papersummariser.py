from metaphor_python import Metaphor
import openai
import os
import datetime
import requests
from pypdf import PdfReader
import re
from pathlib import Path

#Off the bat, this is a fairly simple project. All I need is to grab the appropriate links from arXiv within CV
#and transform them into simple summaries.

#The evolution of it is to be able to grab items from the paper itself.

openai.api_key = os.getenv("OPENAI_API_KEY")
metaphor = Metaphor(os.getenv("METAPHOR_API_KEY"))

metaphor_prompt = "Most recent preprints on computer vision on arXiv."

start_search = datetime.datetime.today() - datetime.timedelta(days=7)

# search_response = metaphor.search(
#     query=metaphor_prompt, use_autoprompt=True, start_published_date=str(start_search.date()), num_results=10
# )

# paper_abstracts = [f"{paper.title}\n {paper.extract}" for paper in search_response.get_contents().contents]

# print(paper_abstracts)

# SYSTEM_MESSAGE = "You are a helpful assistant that summarises recent computer vision papers from their abstracts. Please summarise the following papers."

# completion = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": SYSTEM_MESSAGE},
#         {"role": "user", "content": " ".join(paper_abstracts)},
        
#     ],
# )

# print(completion.choices[0].message.content)

#I'd like to point out that everything I'm doing here is entirely trivial. I totally get that, considering
#that it's really no different than the example that's already shown in the docs. But consider the following:
#One of Metaphor's greatest strengths is being able to search the internet using natural language queries. But
#metaphor currently isn't quite as capable of retrieving information beyond the text contents that can be extracted
#from a website for processing in an LLM.

#This is all well and good, but the modern website contains so much more than just text nowadays. Even in the simple
#example of arXiv which is arguably *all* text, the only readily-available text is the Abstract itself, with the rest
#being contained within the attached pdf, or perhaps the appendix items like graphs and other images.

#So how do we go about making Metaphor even more powerful?

#I think that structured queries like GraphQL can be incredibly powerful; while sometimes you may not know what you're
#looking for when searching the internet, but sometimes you know exactly what to expect, and being able to structure
#the data that you're about to receive could be supremely useful. For example, what if you wanted to retrieve all
#the images 

def metaphor_multi_media(query, autoprompt=True, num_results=1, start_publish_date=None, get_images=False):


    search_response = metaphor.search(
        query=query, use_autoprompt=autoprompt, start_published_date=start_publish_date, num_results=num_results
    )

    abstracts = [f"{paper.title}\n {paper.extract}" for paper in search_response.get_contents().contents]

    message = "You are a helpful assistant that summarises recent computer vision papers from their abstracts. Summarise the following papers."

    if get_images:

        message += "Tell the user that the images within the pdf have been saved locally."

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": message},
            {"role": "user", "content": " ".join(abstracts)},
            
        ],
    )

    if get_images:

        pdf = re.sub(r"abs", "pdf", search_response.get_contents().contents[0].url) + ".pdf"

        filename = Path("paper.pdf")

        response = requests.get(pdf)

        filename.write_bytes(response.content)

        reader = PdfReader(filename)

        count = 0

        for page in reader.pages:
            for image_object in page.images:
                with open(str(count) + image_object.name, "wb") as fp:
                    fp.write(image_object.data)
                    count +=1

        #Somewhere within here is an opportunity to feed these images into another system capable
        #of image description, which would allow our search to delve much deeper into results and
        #not just provide a list of places to go, but also help build a broader understanding of
        #the results without the user even needing to look.

        

    
    
    return completion


response = metaphor_multi_media(
    query=metaphor_prompt, autoprompt=True, start_publish_date=str(start_search), num_results=1, get_images=True
    )

print(response)

        

