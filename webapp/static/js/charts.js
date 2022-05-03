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
function createLineChart(id, url,date) {
$.ajax({
        type: "GET",
        url: url,
        data: {arg: "demo"}, //必须是key-value值
        dataType: "json",
        async: false,
        cache: false,
        success: function (res) {
            lineRes=res;
        }
    });

    var labels=[];
    var dataMap = {};
    var dates=[];

    function getNextDay(d){
        d = new Date(d);
        d = +d + (1000*60*60*24);
        return new Date(d);
    }
    function dataFormatter(obj,k) {
        var tList = ["0", "2", "4", "6","8","10","12","14","16","18","20","22"];
        var temp;
        var day;
        var d=date;
        console.log(date)
        var values=Object.values(obj);
        var res={};
        labels[k]=values[0][k].city;
        for (var n = 0; n < 5; n++) {
            day = d.getMonth() + '-' + d.getDate();
            console.log(day)
            dates[n]=day;
            d = getNextDay(d);
            temp = values[n][k];
            for (var i = 0;i < tList.length; i++) {
            if(res[day]===undefined) res[day]=[];
                res[day][i] = {
                    name: tList[i],
                    value: temp.num[i]
                };
            }
        }
        return res;
    }
    function axisFormatter() {
        var data=[];
        for(var i=0;i<dates.length;i++) {
            if(i%2===0) {
                data[i]={
                        value: dates[i],
                        symbol: 'diamond',
                        symbolSize: 16
                }
            } else {
                data[i]=dates[i];
            }
        }
        return data;
    }

    function optionFormatter() {
        var options=[];
        for(var i=0;i<dates.length;i++) {
            var obj={};
            obj.title={'text':'Heat-'+dates[i]};
            obj.series=[{ 'data': dataMap.city1[dates[i]] },
                    { 'data': dataMap.city2[dates[i]] },
                    { 'data': dataMap.city3[dates[i]] }];
            options[i]=obj;
        }
        return options;
    }
    dataMap.city1 = dataFormatter(lineRes,0);
    dataMap.city2 = dataFormatter(lineRes,1);
    dataMap.city3 = dataFormatter(lineRes,2);

    option = {
        baseOption: {
            timeline: {
                axisType: 'category',
                // realtime: false,
                // loop: false,
                autoPlay: true,
                // currentIndex: 2,
                playInterval: 1000,
                // controlStyle: {
                //     position: 'left'
                // },
                data: axisFormatter(),
                label: { interval: 1 },
            },
            title: {
                subtext: 'XXXX'
            },
            tooltip: {},
            legend: {
                left: 'right',
                data: labels,
            },
            calculable: true,
            grid: {
                top: 80,
                bottom: 100
            },
            xAxis: [
                {
                    type: 'category',
                    axisLabel: { interval: 0 },
                    data: ["0", "2", "4", "6","8","10","12","14","16","18","20","22"],
                    splitLine: { show: false }
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    name: 'Heat',
                    max: 100
                }
            ],
            series: [
                { name: labels[0], type: 'line' },
                { name: labels[1], type: 'line' },
                { name: labels[2], type: 'line' }
            ]
        },
        options: optionFormatter()
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
            xList = res.city;
            yList = res.values1;
            zList = res.values2;
        }
    });
    option = {
        title: {
            text: 'Emotion Over Cities',
            left: 'center'
        },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {
        data: ['positive','negative']
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: [
        {
          type: 'value'
        }
      ],
      yAxis: [
        {
          type: 'category',
          axisTick: {
            show: true
          },
          data: xList
        }
      ],
      series: [
        {
          name: 'Positive',
          type: 'bar',
          stack: 'Total',
          label: {
            show: true
          },
          emphasis: {
            focus: 'series'
          },
          data: yList
        },
        {
          name: 'Negative',
          type: 'bar',
          stack: 'Total',
          label: {
            show: true,
            position: 'left'
          },
          emphasis: {
            focus: 'series'
          },
          data: zList
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
            text: 'Heat Over Cities',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'left'
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
                rows = res.rows;

            }
        });

        option = {
            title: {
                text: 'Word Cloud',
                left: 'center'
            },
            tooltip: {},
            series: [ {
                type: 'wordCloud',
                gridSize: 2,
                sizeRange: [12, 50],
                rotationRange: [-90, 90],
                shape: 'pentagon',
                width: 600,
                height: 400,
                drawOutOfBound: false,
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
                data: rows
            } ]
        };
        cloud = echarts.init(document.getElementById(id));
        option && cloud.setOption(option);
}

//PagebarChart
function createPageBarChart(id, url) {
    $.ajax({
        type: "GET",
        url: url,
        data: {arg: "demo"}, //必须是key-value值
        dataType: "json",
        async: false,
        cache: false,
        success: function (res) {
            xList = res.keyword;
            yList = res.values;

            highlightList = res.highlights;
        }
    });
    for (var i = 0; i < yList.length; i++) {
        if (highlightList[i] === true) {
            yList[i] = {
                value: yList[i],

            };

        }
    }
    option = {
        tooltip:{},
        legend: {
            data: ['wordcount'],
            align: 'left',
            left: 20,
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
                name: 'wordcount',
                data: yList,
                // stack: 'one',
                type: 'bar',
                color: '#f7a35c'
            },

        ]
    };
    barChart = echarts.init(document.getElementById(id));
    option && barChart.setOption(option);
}