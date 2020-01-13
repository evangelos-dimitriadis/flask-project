const get_benchmarks_names = './api/get_benchmarks';

window.onload =  function(){
    createColapseButtons();
    //createTable();
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

function insertAfter(referenceNode, newNode) {
    referenceNode.parentNode.insertBefore(referenceNode.nextSibling, newNode);
}

function insertBefore(referenceNode, newNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
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
                        button.setAttribute("onclick", "createTable(\""+`${benchmark}`+"\")");
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
                        //appendNode(wrapper, div); // DEN KLEINEI SWSTA TO /BUTTON
                        insertBefore(wrapper, div)
                        wrapNode(document.getElementById(`${benchmark}`), document.createElement('p'));

                });
            }
        )
        .catch(function(error) {
        // If there is any error you will catch them here
        });   
    });
}

function createTable(benchmark) {
    $.get("table", function( table_html ) {
        // table_html contains whatever that request returned
        // Check if the table exists already. A datatable cannot be initialized twice.
        table_id = String(benchmark) + "_table"
        console.log("benchmark is " + benchmark)
        if (document.getElementById(table_id){
            console.log("already there");
            return
        }
        new_html = table_html.replace("%id%", table_id)
        new_html = new_html.replace("#id", "#" + table_id)
        let div = document.getElementById("collapse"+`${benchmark}`);
        let fragment = document.createRange().createContextualFragment(new_html);
        
        div.appendChild(fragment);


});
}
