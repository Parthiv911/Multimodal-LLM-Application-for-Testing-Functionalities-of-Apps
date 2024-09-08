import os
import time
from typing import List, Tuple, Optional
import google.generativeai as genai
from PIL import Image

GOOGLE_API_KEY =                                                                                       

def get_llm_output(text_prompt,image_prompts):
    #Authenticating and Configuring the Multimodal LLM
    google_key = GOOGLE_API_KEY
    genai.configure(api_key=google_key)
    generation_config = genai.types.GenerationConfig(temperature=1,max_output_tokens=1000)
    model_name = "gemini-1.5-flash"
    model = genai.GenerativeModel(model_name)

    #Obtaining an image example for one short prompting
    image=Image.open("images/startpage.jpeg")
    #Defining the prompt template and inserting context into it
    context=text_prompt
    prompt_template=f"""
    You need to provide testcases to test the functionalities of an app based on screenshots of the app.
    Your output should describe a detailed, step-by-step guide on how to test each functionality. 
    You also have access to the below optional context which may or may not be provided.

    <context start>
    {context}
    <context end> 
        
    Each test case that you write should include:
    1. Description: What the test case is about.
    2. Pre-conditions: What needs to be set up or ensured before testing.
    3. Testing Steps: Clear, step-by-step instructions on how to perform
    the test.
    4. Expected Result: What should happen if the feature works correctly.

    Do not assume any features of the app. Provide testcases only based on the information available in the screenshots.

    An example test case for the last image is as follows:
    1. Description: Verify that the user can enter the location of pick up and drop off,  the date of journey and click submit
    2. Pre-conditions: The screen must be loaded.
    3. Testing Steps: 
        a. Click the From field.
        b. Enter location to be picked from
        c. Close the from field
        d. Click the to field
        e. Enter location to be dropped off
        f. Close the to field
        g. Click the date entry field
        h. Enter date of travel
        i. Close the date field
        j. Click submit
    4. Expected Results: The form should submit

    Now, Find out which image corresponds to the above example and ignore that image. Write testcases for the other images.
    """

    #concatenating text and image prompt
    inputs = [prompt_template]+image_prompts+[image]
    #providing the prompt to llm and obtaining output
    response = model.generate_content(inputs, stream=True, generation_config=generation_config)
    response.resolve()

    #returning the output
    return response._result.candidates[0].content.parts[0].text

#For debugging purposes
if __name__ == "__main__":
    print("google-generativeai:", genai.__version__)
    text_prompt="Explain this"
    image_prompt=Image.open("images/startpage.jpeg")
    
    print(get_llm_output(text_prompt,image_prompt))





