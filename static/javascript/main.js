
function getNextElment() {
  if (is_explore_page)
    var url = "/api/saved";
  else if (is_review_page)
    var url = "/api/data"
  else if (is_main_page)
    var url = "/api/empty";
  else
    console.log('Error!!!')

  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("GET", url, false);
  xmlHttp.send(null);
  return JSON.parse(xmlHttp.responseText);
}

function getContributionsBy(name) {
  $.ajax({
    type: 'POST',
    url: "/api/getCon",
    data: { 'Reviewed by': name }, //How can I preview this?
    dataType: 'json',
    success: function (d) {
      document.getElementById('num_cont').innerHTML = 'Number of Contributions: ' + d.num_cont;
    }
  });
}

function getContributionsNames() {
  var url = "/api/getConNames";
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("GET", url, false);
  xmlHttp.send(null);
  return JSON.parse(xmlHttp.responseText);
}

function setUpBarGraph() {
  // Initialize the echarts instance based on the prepared dom
  var myChart = echarts.init(document.getElementById('main'));
  var contributers = getContributionsNames()
  // Specify the configuration items and data for the chart
  var source = []
  for (var key in contributers) {
    source.push([key, contributers[key]])
  }
  console.log(source)
  var option = {
    dataset: [
      {
        dimensions: ['name', 'contributers'],
        source: source
      },
      {
        transform: [
          {
            type: 'sort',
            config: { dimension: 'contributers', order: 'desc' }
          }
        ]
      }
    ],
    title: {
      text: ''
    },
    tooltip: {},
    legend: {
      data: ['Contributers']
    },
    xAxis: {
      type: 'category'
    },
    yAxis: {},
    series: [
      {
        name: 'Contributers',
        type: 'bar',
        itemStyle: {
          // HERE IS THE IMPORTANT PART
          color: "rgba(13,202,240,1)"
        },
        datasetIndex: 1
      }
    ]
  };

  myChart.setOption(option);
}

function setEmpty() {
  document.getElementById('instruction').value = "";
  document.getElementById('output').value = "";

}

function getNext() {
  element = getNextElment()
  document.getElementById('instruction').value = element['instruction'];
  document.getElementById('output').value = element['output'];
  document.getElementById('index_input').value = element['index'];
  document.getElementById('index').innerHTML = 'index: ' + element['index'];
  document.getElementById('Reviewed by').value = curr_reviewer
  console.log("Current Reviewer", curr_reviewer)

  if (is_explore_page) {
    setUpBarGraph();
  }
}

$(".edittable").on('change', function () {
  changed = true
});

$(".changed").on('change', function () {
  curr_reviewer = this.value
});

function checkChanges() {
  if (!changed) {
    $('#exampleModal').modal('show');
  } else {
    submitForm()
  }
}

function submitForm() {
  document.getElementById('theForm').submit();
  num_cont += 1
}

$(document).on('submit', '#theForm', function (e) {
  e.preventDefault();
  $.ajax({
    type: 'POST',
    url: '/api/submit',
    data: $('form').serialize(),
    success: function () {
      getNext();
      getContributionsBy(curr_reviewer)

    }
  })
});

num_cont = 0
curr_reviewer = ""
changed = true

is_explore_page = window.location.pathname == '/explore'
is_review_page = window.location.pathname == '/review'
is_main_page = window.location.pathname == '/'

if (is_explore_page) {
  $('#btnSubmit').hide();
  $('#btnClear').hide();
  $('#num_cont').hide();
} else if (is_main_page) {
  $('#btnSkip').hide();
}
getNext();


