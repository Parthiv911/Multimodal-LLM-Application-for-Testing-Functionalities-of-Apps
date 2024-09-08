from flask import Flask,render_template,request,jsonify
from PIL import Image
from llm import get_llm_output
app = Flask(__name__)

#Create the root route
@app.route("/")
def hello_world():
    return render_template("index.html")

#The HTML page at root will request the frontend.js, provide it when requested
@app.route("/frontend.js")
def js():
    return render_template("frontend.js")

#Define the llm endpoint that the front-end sends the images and optional context to for processing by llm
@app.route("/llm",methods=["POST"])
def llm_processing():
    #extract the image files 
    files=[]
    for i in range(len(request.files)):
        files.append(request.files.get("files"+str(i)))
    
    #open the image files and obtain the images
    images=[]
    for i in range(len(files)):
        images.append(Image.open(files[i]))

    #obtain the optional context
    text_prompt=request.form.get("context")

    #provide the images and context to the multimodal llm for generation of testcases
    llm_output=get_llm_output(text_prompt,images)

    print(llm_output)
    #send the generated content as server response to front-end
    return jsonify({"llm_output":llm_output})
app.run()