const get_benchmarks_names = './api/get_benchmarks';

window.onload =  function(){
    createColapseButtons();
    createTable();
};

function createNode(element) {
    return document.createElement(element); // Create the type of element you pass in the parameters
}

function appendNode(parent, element) {
    return parent.appendChild(element); // Append the second parameter(element) to the first one
}

function wrapNode(element, wrapper) { // Wrap the given element into another element
    element.parentNode.insertBefore(wrapper, element);
    wrapper.appendChild(element);
}

console.log(get_benchmarks_names)

function createColapseButtons() {
    fetch(get_benchmarks_names)
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
                return benchmarks.map(function(benchmark) { // Map through the results and for each run the code
                        let button = createNode('button')
                        
                        //Assign different attributes to the element.
                        button.setAttribute("class", "btn btn-primary");
                        button.setAttribute("type", "button");
                        button.setAttribute("id", `${benchmark}`);
                        button.setAttribute("data-toggle", "collapse");
                        button.setAttribute("data-target", "#collapse"+`${benchmark}`);
                        button.setAttribute("aria-expanded", "false");
                        button.setAttribute("name", "collapse"+`${benchmark}`);
                        button.innerHTML = "Show " + `${benchmark}` + " table" ;
                        appendNode(document.body,button);

                        let div = createNode('div')
                        div.setAttribute("class", "collapse");
                        div.setAttribute("id", "collapse"+`${benchmark}`);
                        let wrapper = document.getElementById(`${benchmark}`);
                        console.log(wrapper)
                        appendNode(wrapper, div);
                        
                        wrapNode(document.getElementById(`${benchmark}`), document.createElement('p'));

                });
            }
        )
        .catch(function(error) {
        // If there is any error you will catch them here
        });   
    });
}

function createTable() {
    $.get("table", function( table_html ) {
        // table_html contains whatever that request returned
        new_html = table_html.replace("%id%", "new_table")
        new_html = new_html.replace("#id", "#new_table")
        let div = document.getElementById("edw");
        const fragment = document.createRange().createContextualFragment(new_html);
        console.log(new_html)
        //div.insertAdjacentHTML('beforeend', table_html);
        
        div.appendChild(fragment);

        
});
}
