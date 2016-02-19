var data = {
    labels: ["09.Jan.2016", "10.Jan.2016", "21.Jan.2016", "01.Feb.2016", "10.Feb.2016"],
    datasets: [
        {
            label: "Weight (kg)",
            fillColor: "rgba(164,196,0,0.2)",
            strokeColor: "rgba(164,196,0,1)",
            pointColor: "rgba(164,196,0,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(164,196,0,1)",
            data: [75, 76, 74, 73, 72]
        },
    ]
};
// Get the context of the canvas element we want to select
var ctx = document.getElementById("myChart").getContext("2d");
var myNewChart = new Chart(ctx).Line(data);
