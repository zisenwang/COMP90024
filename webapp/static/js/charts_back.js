var option;
var xList;
var yList;
var zList;
var highlightList;
var sections;
var lineRes;

var lineChart;
var barChart;
var pieChart;
var cloud;
//lineChart
function createLineChart(id, url) {
    $.ajax({
        type: "GET",
        url: url,
        data: {arg: "demo"}, //必须是key-value值
        dataType: "json",
        async: false,
        cache: false,
        success: function (res) {
            lineRes=res.rows;
        }
    });
    var labels=[];
    var series=[];
    for (var i = 0; i < lineRes.length; i++) {
        labels.push(lineRes[i].city);
        series.push({
                'data': lineRes[i].num,
                'name': lineRes[i].city,
                'type': 'line'
            });
    }
    console.log(labels);
    option = {
        legend:{
        data: labels,
        align: 'left',
        left: 20,
        },
        xAxis: {
            type: 'category',
            data: ["0", "2", "4", "6","8","10","12","14","16","18","20","22"]
        },
        yAxis: {
            type: 'value'
        },
        series: series
    };
    lineChart = echarts.init(document.getElementById(id));
    option && lineChart.setOption(option);
}

//barChart
function createBarChart(id, url) {
    $.ajax({
        type: "GET",
        url: url,
        data: {arg: "demo"}, //必须是key-value值
        dataType: "json",
        async: false,
        cache: false,
        success: function (res) {
            xList = res.days;
            yList = res.values1;
            zList = res.values2;
            highlightList = res.highlights;
        }
    });
    for (var i = 0; i < yList.length; i++) {
        if (highlightList[i] === true) {
            yList[i] = {
                value: yList[i],
                itemStyle: {
                    color: '#f45b5b'
                }
            };
            if (highlightList[i] === true) {
                zList[i] = {
                    value: zList[i],
                    itemStyle: {
                        color: '#058DC7'
                    }
                };
            }
        }
    }
    option = {
        legend: {
            data: ['positive', 'negative'],
            align: 'left',
            left: 20
        },
        xAxis: {
            type: 'category',
            data: xList
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name: 'positive',
                data: yList,
                // stack: 'one',
                type: 'bar',
                color: '#f7a35c'
            },
            {
                name: 'negative',
                data: zList,
                // stack: 'one',
                type: 'bar',
                color: '#8085e9'
            }
        ]
    };
    barChart = echarts.init(document.getElementById(id));
    option && barChart.setOption(option);
}

//pieChart
function createPieChart(id, url) {
    $.ajax({
        type: "GET",
        url: url,
        data: {arg: "demo"}, //必须是key-value值
        dataType: "json",
        async: false,
        cache: false,
        success: function (res) {
            sections = res.rows;
        }
    });
    option = {
        title: {
            text: 'Heat over the Citys',
            subtext: 'XXXXXXXXX',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            align: 'right',
            right: 10
        },
        series: [
            {
                name: 'Access From',
                type: 'pie',
                radius: '50%',
                data: sections,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
    pieChart = echarts.init(document.getElementById(id));
    option && pieChart.setOption(option);
}
    //cloud
    function createCloud(id, url) {
        $.ajax({
            type: "GET",
            url: url,
            data: {arg: "demo"}, //必须是key-value值
            dataType: "json",
            async: false,
            cache: false,
            success: function (res) {
                sections = res.sections;
                highlightList=res.highlights;
            }
        });
        for(var i=0;i<sections.length;i++) {
            if (highlightList[i]===true) {
                sections[i]["textStyle"] = {'color': 'black'};
                sections[i]["emphasis"] = {'textStyle': {'color': 'red'}};
            }
        }
        option = {
            series: [ {
                type: 'wordCloud',
                gridSize: 2,
                sizeRange: [12, 50],
                rotationRange: [-90, 90],
                shape: 'pentagon',
                width: 600,
                height: 400,
                drawOutOfBound: true,
                textStyle: {
                    color: function () {
                        return 'rgb(' + [
                            Math.round(Math.random() * 160),
                            Math.round(Math.random() * 160),
                            Math.round(Math.random() * 160)
                        ].join(',') + ')';
                    }
                },
                emphasis: {
                    textStyle: {
                        shadowBlur: 10,
                        shadowColor: '#333'
                    }
                },
                data: sections
            } ]
        };
        cloud = echarts.init(document.getElementById(id));
        option && cloud.setOption(option);
}
