
var arr = [
    {
        label:"Bulbasaur",
        link:"/001"
    },
    {
        label:"Ivysaur",
        link:"/2"
    },
    {
        label:"Floatzel",
        link:"/419"
    }
];


$(document).ready(function() {

    var listData=[];

    //load the relevant data into the array
    $.getJSON("../static/database/pokedex.json", function(data){
        for(i=0;i<649;i++){
            var temp = {label: data[i]['ename'], link: "/"+data[i]['id']};
            listData.push(temp);
        }

        //want alphabetical order
        listData.sort(function(a, b){

            //lowercase all names to avoid unintended results
            var nameA = a.label.toLowerCase();
            var nameB = b.label.toLowerCase();

            if(nameA<nameB){
                return -1;
            }
            else if(nameA>nameB){
                return 1;
            }
            else{
                return 0;
            }
        });

    });

    

    
    //show suggestions in alphabetical order
    $("input#autocomplete").autocomplete({
        source: listData,
        select: function( event, ui ) { 
            window.location.href = ui.item.link;
        }
    });
});