document.getElementById("aform").addEventListener("submit", e=>{
    //prevents refresh on submitting the html form
    e.preventDefault();

    //Obtain the files uploaded and the optional context
    file=document.getElementById("screenshots");
    text=document.getElementById("context").value;
    
    //Create FormData object to pass as body to the POST request
    const formData = new FormData();
    
    //Insert the text and the files
    formData.append("context",text);
    for (let i=0;i<2;i++){
        formData.append("files"+i,file.files[i]);
    }
    
    //Send the POST request to /llm endpoint
    response=fetch("/llm", {
    method: "POST",
    body: formData
    })
    .then(response => response.json())
    .then(data => {
        //obtain the generated output from the llm app and display it on the html webpage
        document.getElementById("responsefromllm").innerHTML=data.llm_output;
    });

});