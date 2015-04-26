/**
 * Created by juanlu on 29/03/15.
 */
google.load("visualization", "1", {packages:["corechart"]});

function drawChart(arrayofarray, title, id) {
    var data = google.visualization.arrayToDataTable(arrayofarray);
    var options = {
      title: title
    };
    var chart = new google.visualization.PieChart(document.getElementById(id));
    chart.draw(data, options);
}

function drawBasic(arrayofarray, title, id) {

      var data = google.visualization.arrayToDataTable(arrayofarray);

      var options = {
        title: title,
        chartArea: {width: '60%'}
      };

      var chart = new google.visualization.BarChart(document.getElementById(id));

      chart.draw(data, options);
}

function columnChart(arrayofarray, title, id) {

      var data = google.visualization.arrayToDataTable(arrayofarray);

      var options = {
        title: title,
        chartArea: {width: '60%'}
      };

      var chart = new google.visualization.ColumnChart(
        document.getElementById(id));

      chart.draw(data, options);
}

function lineChart(arrayofarray, title, id) {
      var data = google.visualization.arrayToDataTable(arrayofarray);

      var options = {
        title: title,
        chartArea: {width: '60%'}
      };

      var chart = new google.visualization.LineChart(document.getElementById(id));
      chart.draw(data, options);
}