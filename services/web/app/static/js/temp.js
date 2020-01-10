document.getElementById("temp_button").onclick = function() {myFunction()};


function myFunction() {
  document.getElementById("text").innerText = Date();
}

function createNode(element) {
    return document.createElement(element); // Create the type of element you pass in the parameters
}

function append(parent, el) {
    return parent.appendChild(el); // Append the second parameter(element) to the first one
}

const url = './api/get_benchmarks';
console.log(url)

fetch(url)
    .then(
        function(response) {
            if (response.status !== 200) {
                console.log('Looks like there was a problem. Status Code: ' +
                response.status);
                return;
            }
            // Examine the text in the response
            response.json().then(function(data) {
            console.log(data)
            
            let benchmarks = data.results
            return benchmarks.map(function(benchmark) { // Map through the results and for each run the code below
                    console.log(benchmark)
                    let li = createNode('li')
                    var newDiv = document.createElement("div"); 
                    // and give it some content 
                    var newContent = document.createTextNode("Hi there and greetings!"); 
                    // add the text node to the newly created div
                    newDiv.appendChild(newContent);
                    // add the newly created element and its content into the DOM 
                    var currentDiv = document.getElementById("text"); 
                    document.body.insertAfter(newDiv, currentDiv)
                    /*
                    let li = createNode('li'), //  Create the elements we need
                        //img = createNode('img'),
                        span = createNode('span');
                    //img.src = benchmarks.picture.medium;  // Add the source of the image to be the src of the img element
                    span.innerHTML = `${benchmark}`; // Make the HTML of our span to be the first and last name of our benchmarks
                    //append(li, img); // Append all our elements
                    append(li, span);
                    append(ul, li);*/
            });
        }
    )
    .catch(function(error) {
    // If there is any error you will catch them here
    });   
});
    
