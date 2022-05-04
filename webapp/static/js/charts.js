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
var map;

function axisFormatter(arr) {
        var data=[];
        for(var i=0;i<arr.length;i++) {
            if(i%2===0) {
                data[i]={
                        value: arr[i],
                        symbol: 'diamond',
                        symbolSize: 16
                }
            } else {
                data[i]=arr[i];
            }
        }
        return data;
}
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
        var values=Object.values(obj);
        var res={};
        labels[k]=values[0][k].city;
        for (var n = 0; n < 5; n++) {
            day = d.getMonth() + '-' + d.getDate();
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

    function optionFormatter() {
        var options=[];
        for(var i=0;i<dates.length;i++) {
            var obj={};

            obj.title={'text':'Heat During the Day','subtext': 'date ('+(date.getYear()+1900) + '-'+dates[i]+')',left: 'center'};
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
                data: axisFormatter(dates),
                label: { interval: 1 },
            },
            tooltip: {},
            legend: {
                left: 'right',
                data: labels,
                orient: 'vertical'
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
            right: 'right',
            formatter:function(name){
                li=name.split(' ');
			    return li[0];
            }
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
        title: {
                text: 'Frequency of Words',
                left: 'center'
            },
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
                color:'#00ADB5'
            },

        ]
    };
    barChart = echarts.init(document.getElementById(id));
    option && barChart.setOption(option);
}
function createMap(id) {

    $.get('http://localhost:8888/static/images/mel_map.svg', function (svg) {
        echarts.registerMap('mel_map', { svg: svg });
        option = {
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
                data: axisFormatter(['1','2','3','4','5']),
                label: { interval: 1 },
           },
            tooltip: {},
            geo: {
                tooltip: {
                    show: true
                },
                map: 'mel_map',
                roam: true
            },
            series: {
                type: 'effectScatter',
                coordinateSystem: 'geo',
                geoIndex: 0,
                symbolSize: function (params) {
                    return (params[2] / 100) * 15 + 5;
                },
                itemStyle: {
                    color: '#b02a02'
                },
                encode: {
                    tooltip: 2
                },
                data: [
                    [488, 459, 100],
                    [600, 600, 30],
                    [500, 500, 40],
                    [770.3415644319939, 757.9672194986475, 30],
                    [1180.0329284196291, 743.6141808346214, 80],
                    [894.03790632245, 1188.1985153835008, 61],
                    [1372.98925630313, 477.3839988649537, 70],
                    [1378.62251255796, 935.6708486282843, 81]
                ]
            }
        };
        map = echarts.init(document.getElementById(id));
        map.setOption(option);
        map.getZr().on('click', function (params) {
            var pixelPoint = [params.offsetX, params.offsetY];
            var dataPoint = map.convertFromPixel({ geoIndex: 0 }, pixelPoint);
        });
    });
}

//suburb pie chart
function createSuburbPieChart(id, url) {
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
            text: 'Heat Over Suburb',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        series: [{
            name: 'Access From',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: true,
            itemStyle: {
                borderRadius: 5,
                borderColor: '#fff',
                borderWidth: 2
            },

            data: sections
        }]
    };
    pieChart = echarts.init(document.getElementById(id));
    option && pieChart.setOption(option);
}

//page sunburst
function createSunburst(id, url) {
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
            text: 'Emotion',
            left: 'left'
        },
        tooltip: {

        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        visualMap: {
            type: 'continuous',
            min: 0,
            max: 100,
            inRange: {
              color: ['#2F93C8', 'rgba(248, 246, 246, 1)', '#F98862']
            }
          },
        series: {
            type: 'sunburst',
            data: sections,
            radius: ['15%', '90%'],
            label: {
                rotate: 'radial',
                color:'rgba(248, 246, 246, 1)'
            },
             itemStyle: {
                borderWidth: 2
            },
        }
    };
    sunburstChart = echarts.init(document.getElementById(id));
    option && sunburstChart.setOption(option);
}
