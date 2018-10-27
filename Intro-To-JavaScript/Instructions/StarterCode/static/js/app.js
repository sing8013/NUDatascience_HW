// from data.js
var tableData = data;

//debugger

// YOUR CODE HERE!
//console.log(tableData);

// Get Reference to the table body
var tbody=d3.select("tbody")

//create function to create row and tabulated data
function add2table(element) {
    //add row of data
    var row = tbody.append("tr");
    //add cells for each category
    row.append("td").text(element.datetime).classed('datetime',true);
    row.append("td").text(element.city).classed('city',true);
    row.append("td").text(element.state).classed('state',true);
    row.append("td").text(element.country).classed('country',true);
    row.append("td").text(element.shape).classed('shape',true);
    row.append("td").text(element.durationMinutes).classed('durationMinutes',true);
    row.append("td").text(element.comments).classed('comments',true);

};


//Get Reference to the filter button
var filterButton = d3.select("#filter-btn");

filterButton.on("click",function(){
    //prevent the page from refreshing
    d3.event.preventDefault();

    //clear existing table rows
    tbody.selectAll("tr").remove();

    //Get reference to input filter date
    let inputFilter = d3.select(".form-control").property("value");
    console.log(`input filter: ${inputFilter}`);

    //filered data
    filetered_tableData = tableData.filter(element=> element.datetime===inputFilter);
    console.log(filetered_tableData);
    filetered_tableData.forEach(element=> add2table(element))

     //update the filter options
     refresh_filters(false);
});

//------------------------------------------------------------------------------------
//Create event function to update table based on any filter selection

d3.selectAll("select").on("change",function(){
    
    d3.event.preventDefault();

    

    console.log('#################')
    filter_val=d3.event.target.value;
    filter_class=this.id.split(" ")[1];
    console.log(`${filter_class}  ${filter_val}`)
    console.log(tbody)
    
    //collect current table data loaded in HTML
    dict=[]
    var table = tbody._groups[0][0];

    for (i=0;i<table.rows.length;i++) {
        var vars={}
        for(j=0;j<table.rows[i].cells.length;j++){
            key=table.rows[i].cells[j].className;
           // vars[j].key = table.rows[i].cells[j].className;
            vars[key] = table.rows[i].cells[j].textContent;
        }
        dict.push(vars)
    }

    console.log(dict)
    //rows.map(node=> 
    //    console.log(node)
    //    dict.push({
    //         'datetime': node.childnodes[0].textContent,
    //         'city': node.childnodes[1].textContent,
    //         'state': node.childnodes[2].textContent,
    //         'country': node.childnodes[3].textContent,
    //         'shape': node.childnodes[4].textContent,
    //         'durationMinutes':node.childnodes[5].textContent,
    //         'comments': node.childnodes[6].textContent,
    //         })
  //  )
   // console.log(node)
   // console.log(dict)

    //clear existing table rows
    tbody.selectAll("tr").remove();

    //filered data
    filetered_tableData = tableData.filter(element=> element[filter_class]===filter_val);
    console.log(filetered_tableData);
    filetered_tableData.forEach(element=> add2table(element))

    //update the filter options
    refresh_filters(true);

})


//Create function to refresh all filters with current selection
function refresh_filters(retainSelection){
    //loop through all select options
    var all_filters = d3.selectAll("select")._groups[0];
    console.log(all_filters);
    console.log('******************')
    count=0

    all_filters.forEach(function(item){
        //d3.event.preventDefault()
        //console.log(item.value);
        count+=1
        console.log(`updating filter ${count}`)
        //determine the event id
        filter_class=item.id.split(" ")[1];
        console.log(`filter activated: ${filter_class}`);

        //get list of unique options from current table body
        var arrLS=[];
        var ls = tbody.selectAll("td").filter(`.${filter_class}`)._groups[0];
        //add to list
        ls.forEach(x=>arrLS.push(x.textContent));
        var uniqueLS = arrLS.filter(function(item, i, ar){ return ar.indexOf(item) === i; });
        
        if (retainSelection==false){
            //add blank as first option
            uniqueLS.unshift("");
        }

        //arrLS = arrLS.unique();
        //console.log(arrLS);
        console.log(uniqueLS)

        //Populate the list of options to the select
        console.log(item)

       var thisFilter = d3.select(item) //d3.selectAll("select").filter(`#exampleFormControlSelect1 ${filter_class}`);
       console.log('------------------')
       console.log(thisFilter);

       //clear current options
       thisFilter.selectAll("option").remove();
       
       // load new options to select
       uniqueLS.forEach(x=> thisFilter.append("option")
                            .attr("class",`${filter_class} ${x}`)
                            .attr("value",x)
                            .text(x))
                            
    })
};

// Loop through tableData and add row and add all keys:
// Default
tableData.forEach(element => add2table(element));
 //update the filter options
 refresh_filters(false);