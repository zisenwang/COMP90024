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
var radar;
var dates=[];

var dict=[
    [200, 520],
    [200, 300],
    [350, 200],
    [570, 170],
    [725, 250],
    [1040, 350],
    [1000, 700],
    [570, 1000],
    [780, 750],
    [660, 780],
    [680, 650],
    [600, 620],
    [530, 580],
    [550, 530],
    [640, 530],
    [740, 520],
    [740, 430],
    [650, 460],
    [570, 450],
    [550, 490],
    [490, 480],
    [480, 440],
    [510, 430],
    [370, 480],
    [410, 420],
    [350, 380],
    [430, 370],
    [480, 360],
    [520, 360],
    [580, 360],
    [680, 390]
]

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
function createLineChart(id, url,date,max) {
    $.ajax({
        type: "GET",
        url: url,
        data: {arg: "demo"}, //必须是key-value值
        dataType: "json",
        async: false,
        cache: true,
        success: function (res) {
            lineRes=res;
        }
    });

    var labels=[];
    var dataMap = {};

    function dataFormatter(obj,k) {
        var tList = ["0", "2", "4", "6","8","10","12","14","16","18","20","22"];
        var temp;
        var day;
        var values=Object.values(obj);
        var res={};
        labels[k]=values[0][k].city;
        for (var n = 0; n < 5; n++) {
            dates[n]=Object.keys(obj)[n];
            temp = values[n][k];
            for (var i = 0;i < tList.length; i++) {
                if(res[dates[n]]===undefined) res[dates[n]]=[];
                res[dates[n]][i] = {
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

            obj.title={'text':'Heat During the Day',textStyle: {
                    fontSize: 20,
                    color:"#44444b",
                    fontFamily:"Comic Sans MS"
                },'subtext': 'date ('+(date.getYear()+1900) + '-'+dates[i]+')',left: 'center'};
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
                autoPlay: true,
                // currentIndex: 2,
                playInterval: 1000,
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
                    max: max
                }
            ],
            series: [
                { name: labels[0], type: 'line' ,stack: 'Total',areaStyle: {},smooth: true,emphasis: {focus: 'series'},itemStyle: {color: '#eed77e'}},
                { name: labels[1], type: 'line' ,stack: 'Total',areaStyle: {},smooth: true,emphasis: {focus: 'series'},itemStyle: {color: '#df9a6c'}},
                { name: labels[2], type: 'line' ,stack: 'Total',areaStyle: {},smooth: true,emphasis: {focus: 'series'},itemStyle: {color: '#dd7e6b'}}
            ]
        },
        options: optionFormatter()
    };
    lineChart = echarts.init(document.getElementById(id));
    option && lineChart.setOption(option);
}
function updateLineChart(url,date,max) {
    var labels=[];
    var dataMap = {};
    $.ajax({
        type: "GET",
        url: url,
        data: {arg: "demo"}, //必须是key-value值
        dataType: "json",
        async: true,
        cache: true,
        success: function (res) {
            lineRes=res;
            dataMap.city1 = dataFormatter(lineRes,0);
            dataMap.city2 = dataFormatter(lineRes,1);
            dataMap.city3 = dataFormatter(lineRes,2);
            option = {
                baseOption: {
                    timeline: {
                        axisType: 'category',
                        autoPlay: true,
                        // currentIndex: 2,
                        playInterval: 1000,
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
                            max: max
                        }
                    ],
                    series: [
                        { name: labels[0], type: 'line' ,stack: 'Total',areaStyle: {},smooth: true,emphasis: {focus: 'series'},itemStyle: {color: '#eed77e'}},
                        { name: labels[1], type: 'line' ,stack: 'Total',areaStyle: {},smooth: true,emphasis: {focus: 'series'},itemStyle: {color: '#df9a6c'}},
                        { name: labels[2], type: 'line' ,stack: 'Total',areaStyle: {},smooth: true,emphasis: {focus: 'series'},itemStyle: {color: '#dd7e6b'}}
                    ]
                },
                options: optionFormatter()
            };
            option && lineChart.setOption(option);
        }
    });
    function dataFormatter(obj,k) {
        var tList = ["0", "2", "4", "6","8","10","12","14","16","18","20","22"];
        var temp;
        var day;
        var values=Object.values(obj);
        var res={};
        labels[k]=values[0][k].city;
        for (var n = 0; n < 5; n++) {
            dates[n]=Object.keys(obj)[n];
            temp = values[n][k];
            for (var i = 0;i < tList.length; i++) {
                if(res[dates[n]]===undefined) res[dates[n]]=[];
                res[dates[n]][i] = {
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

            obj.title={'text':'Heat During the Day',textStyle: {
                    fontSize: 20,
                    color:"#44444b",
                    fontFamily:"Comic Sans MS"
                },'subtext': 'date ('+(date.getYear()+1900) + '-'+dates[i]+')',left: 'center'};
            obj.series=[{ 'data': dataMap.city1[dates[i]] },
                { 'data': dataMap.city2[dates[i]] },
                { 'data': dataMap.city3[dates[i]] }];
            options[i]=obj;
        }
        return options;
    }
}

//barChart
function createBarChart(id, url) {
    $.ajax({
        type: "GET",
        url: url,
        data: {arg: "demo"}, //必须是key-value值
        dataType: "json",
        async: false,
        cache: true,
        success: function (res) {
            xList = res.city;
            yList = res.values1;
            zList = res.values2;
        }
    });
    option = {
        title: {
            text: 'Emotion Over Cities',
            left: 'center',
            textStyle: {
                fontSize: 20,
                color:"#44444b",
                fontFamily:"Comic Sans MS"
            }
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
function updateBarChart(url) {
    $.ajax({
        type: "GET",
        url: url,
        data: {arg: "demo"}, //必须是key-value值
        dataType: "json",
        async: true,
        cache: true,
        success: function (res) {
            xList = res.city;
            yList = res.values1;
            zList = res.values2;
            option = {
                title: {
                    text: 'Emotion Over Cities',
                    left: 'center',
                    textStyle: {
                        fontSize: 20,
                        color:"#44444b",
                        fontFamily:"Comic Sans MS"
                    }
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
            option && barChart.setOption(option);
        }
    });
}

//pieChart
function createPieChart(id, url) {
    $.ajax({
        type: "GET",
        url: url,
        data: {arg: "demo"}, //必须是key-value值
        dataType: "json",
        async: false,
        cache: true,
        success: function (res) {
            sections = res.rows;
        }
    });
    option = {
        title: {
            text: 'Heat Over Cities',
            left: 'center',
            textStyle: {
                fontSize: 20,
                color:"#44444b",
                fontFamily:"Comic Sans MS"
            }
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
function updatePieChart(url) {
    $.ajax({
        type: "GET",
        url: url,
        data: {arg: "demo"}, //必须是key-value值
        dataType: "json",
        async: true,
        cache: true,
        success: function (res) {
            sections = res.rows;
            option = {
                title: {
                    text: 'Heat Over Cities',
                    left: 'center',
                    textStyle: {
                        fontSize: 20,
                        color:"#44444b",
                        fontFamily:"Comic Sans MS"
                    }
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
            option && pieChart.setOption(option);
        }
    });
}

//cloud
function createCloud(id, url) {
    $.ajax({
        type: "GET",
        url: url,
        data: {arg: "demo"}, //必须是key-value值
        dataType: "json",
        async: false,
        cache: true,
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
function updateCloud(url) {
    $.ajax({
        type: "GET",
        url: url,
        data: {arg: "demo"}, //必须是key-value值
        dataType: "json",
        async: true,
        cache: true,
        success: function (res) {
            rows = res.rows;
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
            option && cloud.setOption(option);
        }
    });

}

//PagebarChart
function createPageBarChart(id, url) {
    $.ajax({
        type: "GET",
        url: url,
        data: {arg: "demo"}, //必须是key-value值
        dataType: "json",
        async: false,
        cache: true,
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
            left: 'center',
            textStyle: {
                fontSize: 25,
                color:"#44444b",
                fontFamily:"Comic Sans MS"
            }
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
                color:'#7487a5'
            },

        ]
    };
    barChart = echarts.init(document.getElementById(id));
    option && barChart.setOption(option);
}
function updatePageBarChart(url) {
    $.ajax({
        type: "GET",
        url: url,
        data: {arg: "demo"}, //必须是key-value值
        dataType: "json",
        async: true,
        cache: true,
        success: function (res) {
            xList = res.keyword;
            yList = res.values;
            highlightList = res.highlights;
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
                    left: 'center',
                    textStyle: {
                        fontSize: 25,
                        color:"#44444b",
                        fontFamily:"Comic Sans MS"
                    }
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
            option && barChart.setOption(option);
        }
    });
}

//page sunburst
function createSunburst(id, url) {
    $.ajax({
        type: "GET",
        url: url,
        data: {arg: "demo"}, //必须是key-value值
        dataType: "json",
        async: false,
        cache: true,
        success: function (res) {
            sections = res.rows;
        }
    });
    option = {
        title: {
            text: 'Emotion',
            left: 'left',
            textStyle: {
                fontSize: 25,
                color:"#44444b",
                fontFamily:"Comic Sans MS"
            }
        },
        tooltip: {

        },
        legend: {
            // orient: 'vertical',
            left: 'left'
        },
        visualMap: {
            type: 'continuous',
            min: 0,
            max: 100,
            inRange: {
                color: ['#1a447d', '#aaa594', '#b03b22']
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
function updateSunburst(url) {
    $.ajax({
        type: "GET",
        url: url,
        data: {arg: "demo"}, //必须是key-value值
        dataType: "json",
        async: true,
        cache: true,
        success: function (res) {
            sections = res.rows;
            option = {
                title: {
                    text: 'Emotion',
                    left: 'left',
                    textStyle: {
                        fontSize: 25,
                        color:"#44444b",
                        fontFamily:"Comic Sans MS"
                    }
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
                        color: ['#1a447d', '#aaa594', '#b03b22']
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
            option && sunburstChart.setOption(option);
        }
    });
}

//suburb map
function createMap(id,url,date) {
    $.ajax({
        type: "GET",
        url: url,
        data: {arg: "demo"}, //必须是key-value值
        dataType: "json",
        async: false,
        cache: true,
        success: function (res) {
            mapRes=res;
        }
    });
    function dataFormatter() {
        for (var n = 0; n < 5; n++) {
            dates[n]=Object.keys(mapRes)[n];
        }
        dataMap={}
        for(var i=0;i<dates.length;i++) {
            dataMap[dates[i]]=[];
            for(var j=0;j<dict.length;j++) {
                dataMap[dates[i]][j]=[];
                dataMap[dates[i]][j][0]=dict[j][0];
                dataMap[dates[i]][j][1]=dict[j][1];
                dataMap[dates[i]][j][2]=mapRes[dates[i]][j];
            }
        }
    }
    dataFormatter();
    $.get('../static/images/mel_map.svg', function (svg) {
        echarts.registerMap('mel_map', { svg: svg });
        option = {
//           timeline: {
//                axisType: 'category',
//                autoPlay: true,
//                playInterval: 1000,
//                data: axisFormatter(dates),
//                label: { interval: 1 },
//           },
            tooltip: {},
            geo: {
                tooltip: {
                    show: true
                },
                map: 'mel_map',
                roam: true,
                zoom:1.2
            },
            title: {
                text: 'Heat Distribution',
                textStyle: {
                    fontSize: 20,
                    color:"#44444b",
                    fontFamily:"Comic Sans MS"
                }
            },

            series: {
                type: 'effectScatter',
                coordinateSystem: 'geo',
                geoIndex: 0,
                symbolSize: function (params) {
                    return Math.pow(Math.log(params[2]),2.5)/18;
                },
                itemStyle: {
                    color: '#9e7cd7'
                },
                encode: {
                    tooltip: 2
                },
                data: dataMap[dates[0]]
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
        cache: true,
        success: function (res) {
            sections = res.rows;
        }
    });
    option = {
        title: {
            text: 'Heat Over Suburbs',
            left: 'center',
            textStyle: {
                fontSize: 20,
                color:"#44444b",
                fontFamily:"Comic Sans MS"
            }
        },
        tooltip: {
            trigger: 'item'
        },
        series: [{
            name: 'Access From',
            type: 'pie',
            radius: ['30%', '60%'],
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

//aurin ragar
function createRadar(id) {
    // Schema:
// date,AQIindex,PM2.5,PM10,CO,NO2,SO2
    var dataBreast = [
        {value:[18.38, 214864,17.54, 0.89,35],name:"Melbourne"},
        {value:[16.69,247697,18.48,0.81,45],name:"Sydney"},
        {value:[17.74,70868,15.524,0.86,26],name:"Brisbane"}
        // {value:[16.69,247697,18.48,0.81,45],name:"Sydney", itemStyle: {color: '#F9713C'}},
        // {value:[18.38, 214864,17.54, 0.89,35],name:"Melbourne", itemStyle: {color: '#00ffde'}},
        // {value:[17.74,70868,15.524,0.86,26],name:"Brisbane", itemStyle: {color: '#8000ff'}}
    ];
    var dataColorectal = [
        {value:[15.86,422243,14.4,1.01,58.66],name:"Melbourne"},
        {value:[14.27,485129,14.82,0.91,73],name:"Sydney"},
        {value:[16.051,309987,12.296,1.03,37.75],name:"Brisbane"}
    ];
    var dataLung = [
        {value:[26.1544,422243,23.3,0.83,95],name:"Melbourne"},
        {value:[27.65,485129,28.46,0.87,142],name:"Sydney"},
        {value:[28.64,309987,21.14,0.91,67],name:"Brisbane"}
    ];
    var dataMelanoma = [
        {value:[4.59,510277,4.311,0.7,22],name:"Melbourne"},
        {value:[3.48,584648,3.84,0.592,20.5],name:"Sydney"},
        {value:[5.91,418287,5.7,1,24],name:"Brisbane"}
    ];
    var dataProstate = [
        {value:[22.352,207379,18.43,0.81,35.8],name:"Melbourne"},
        {value:[23.67,237432,20.94,0.867,50],name:"Sydney"},
        {value:[32.32,189488,19.52,1.18,36.5],name:"Brisbane"}
    ];
    var lineStyle = {
        width: 1,
        opacity: 0.5
    };
    option = {
        title: {
            text: 'Cancer Index Over Cities',
            subtext:'Aurin Data',
            right: 'right',
            top:10,
            textStyle: {
                fontSize: 15,
                color:"#44444b",
                fontFamily:"Comic Sans MS"
            }
        },
        tooltip: {
            trigger: 'item',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        textStyle: {
            color: '#4d4d4d'
        },
        legend: {
            orient: 'vertical',
            top:80,
            right: 'right',
            data: ['Breast Cancer', 'Colorectal Cancer', 'Lung Cancer','Melanoma Cancer','Prostate Cancer'],
            itemGap: 20,
            textStyle: {
                color: '#4480b9',
                fontSize: 12
            },
            selectedMode: 'single'
        },
        radar: {
            center: ['45%', '50%'],
            indicator: [
                { name: 'Age-standardised rate', max: 35 },
                { name: 'Relevant\n population', max: 600000 },
                { name: 'Crude rate', max: 30 },
                { name: 'Rate ratio', max: 1.2 },
                { name: 'Mortality', max: 150 }
            ],
            shape: 'circle',
            splitNumber: 5,
            axisName: {
                // color: 'rgb(238, 197, 102)'
            },
            splitLine: {
                lineStyle: {
                    color: [
                        'rgba(0, 48, 84, 0.1)',
                        'rgba(0, 48, 84,  0.2)',
                        'rgba(0, 48, 84,  0.4)',
                        'rgba(0, 48, 84,  0.6)',
                        'rgba(0, 48, 84,  0.8)',
                        'rgba(0, 48, 84,  1)'
                    ].reverse()
                }
            },
            splitArea: {
                show: false
            },
            axisLine: {
                lineStyle: {
                    // color: 'rgba(0, 48, 84,  0.5)'
                }
            }
        },
        series: [
            {
                name: 'Breast Cancer',
                type: 'radar',
                emphasis: {
                    areaStyle: {
                        color: 'rgba(0,250,0,0.3)'
                    }
                },
                lineStyle: lineStyle,
                data: dataBreast,
                symbol:"diamond",
                itemStyle: {
                    // color: '#F9713C'
                },
                areaStyle: {
                    opacity: 0.2
                }
            },

            {
                name: 'Colorectal Cancer',
                type: 'radar',
                emphasis: {
                    areaStyle: {
                        color: 'rgba(0,250,0,0.3)'
                    }
                },
                lineStyle: lineStyle,
                data: dataColorectal,
                symbol: 'diamond',
                itemStyle: {
                    // color: '#B3E4A1'
                },
                areaStyle: {
                    opacity: 0.2
                }
            },

            {
                name: 'Lung Cancer',
                type: 'radar',
                emphasis: {
                    areaStyle: {
                        color: 'rgba(0,250,0,0.3)'
                    }
                },
                lineStyle: lineStyle,
                data: dataLung,
                symbol: 'diamond',
                itemStyle: {
                    // color: 'rgb(238, 197, 102)'
                },
                areaStyle: {
                    opacity: 0.2
                }
            },

            {
                name: 'Melanoma Cancer',
                type: 'radar',
                emphasis: {
                    areaStyle: {
                        color: 'rgba(0,250,0,0.3)'
                    }
                },
                lineStyle: lineStyle,
                data: dataMelanoma,
                symbol: 'diamond',
                itemStyle: {
                    // color: 'rgb(238, 197, 102)'
                },
                areaStyle: {
                    opacity: 0.2
                }
            },

            {
                name: 'Prostate Cancer',
                type: 'radar',
                emphasis: {
                    areaStyle: {
                        color: 'rgba(0,250,0,0.3)'
                    }
                },
                lineStyle: lineStyle,
                data: dataProstate,
                symbol: 'diamond',
                itemStyle: {
                    // color: 'rgb(238, 197, 102)'
                },
                areaStyle: {
                    opacity: 0.2
                }
            }
        ]
    };
    radar = echarts.init(document.getElementById(id));
    option && radar.setOption(option);
}

//aurin boxplot
function createboxplot(id) {
    option = {
        title: [
            {
                text: 'Rental Affordability Index Over Cities',
                left: 'center',
                textStyle: {
                    fontSize: 20,
                    color:"#44444b",
                    fontFamily:"Comic Sans MS"
                }
            },
            {
                text: 'RAI = (Median Income ∕ Qualifying Income) x 100',
                borderColor: '#999',
                borderWidth: 1,
                textStyle: {
                    fontWeight: 'normal',
                    fontSize: 14,
                    lineHeight: 20
                },
                left: '10%',
                top: '90%'
            }
        ],
        dataset: [
            {
                source: [
                    [92.116855, 62.339265, 73.520225, 93.66498, 107.6555, 96.57138, 106.61875, 92.455625, 93.873495, 89.03706, 84.104035, 97.811675, 87.47522, 84.915085, 72.687725, 70.43928, 78.76909, 74.51923, 82.714045, 100.7745, 77.70801, 94.23077, 66.53275, 94.839335, 105.42905, 90.49774, 73.976655, 73.505315, 70.107375, 80.45526],
                ]
            },
            {
                source: [
                    [80.622015, 111.77885, 99.889035, 83.519675, 94.40559, 90.835635, 88.030505, 99.125895, 85.14268, 91.90645, 86.53846, 93.55509, 77.02874, 65.10795, 89.5292, 114.13045, 108.1731, 92.749355, 83.17047, 77.56625	, 76.690395, 94.475865, 81.81428, 79.88166, 89.218855, 83.883285, 83.834135, 105.9655],
                ]
            },
            {
                source: [
                    [124.1629, 113.4379, 97.87819, 117.3734, 105.4034, 115.69455, 123.99895, 119.26585, 130.74245, 107.93645, 128.3253, 131.20065, 138.2205, 120.33105, 128.5177, 121.1165, 96.449985, 119.9323, 122.74895, 121.45075, 117.57375, 112.10375, 139.3563, 101.141435, 127.72965, 141.44105, 107.2326, 102.64925, 118.19625, 106.55915, 102.77595, 117.70485, 95.1874, 121.2208, 131.17895, 118.20765, 118.1915, 86.51074, 106.04545, 98.51435, 109.96745, 113.3433, 119.9741, 140.3665, 129.7352, 105.25315, 121.0635, 97.133995, 127.6857, 93.964335, 123.1901, 126.7507, 124.6398, 123.135, 119.07815, 123.2218, 121.06765, 159.70285, 119.82065, 137.0806, 118.33225, 122.72805, 113.22185, 156.3106, 119.14175, 109.32095, 116.78155, 120.309505, 123.1017, 132.39625, 131.6172, 112.31925, 139.9697, 162.62915, 119.53765, 101.41633, 130.9847, 110.237, 102.410725, 111.2924, 113.1897, 110.14595, 107.531, 112.5466, 104.5111, 92.264875, 104.1051, 113.28565, 101.001905, 105.68245, 181.7218, 132.46305, 151.7694, 168.55725, 168.80285, 165.99895, 137.2315, 139.1573, 77.772045, 103.37575, 127.83185, 140.24385, 132.44055, 137.034, 120.2057, 132.96665, 149.67035, 127.00395, 149.44745, 123.70215, 150.88185, 124.5995],
                ]
            },
            {
                fromDatasetIndex: 0,
                transform: {
                    type: 'boxplot',
                    config: { itemNameFormatter: 'Melbourne' }
                }
            },
            {
                fromDatasetIndex: 1,
                transform: {
                    type: 'boxplot',
                    config: { itemNameFormatter: 'Sydney' }
                }
            },
            {
                fromDatasetIndex: 2,
                transform: {
                    type: 'boxplot',
                    config: { itemNameFormatter: 'Brisbane' }
                }
            },

        ],
        tooltip: {

        },
        grid: {
            left: '10%',
            right: '10%',
            bottom: '22%'
        },
        xAxis: {
            type: 'category',
            boundaryGap: true,
            nameGap: 30,
            splitArea: {
                show: false
            },
            splitLine: {
                show: false
            }
        },
        yAxis: {
            type: 'value',
            name: 'RAI',
            splitArea: {
                show: true
            }
        },
        series: [
            {
                name: 'boxplot',
                type: 'boxplot',
                datasetIndex: 3,
                color:'red',
                markLine: {
                    data: [{ name: 'Rental Affordability Index = 100', yAxis: 100 }]
                }
            },
            {
                name: 'boxplot',
                type: 'boxplot',
                datasetIndex: 4,
                color:'green'
            },
            {
                name: 'boxplot',
                type: 'boxplot',
                datasetIndex: 5
            }
        ]
    };
    boxplotChart = echarts.init(document.getElementById(id));
    option && boxplotChart.setOption(option);
}

//aurin health scenario bar chart
function createHorBarplot(id) {
    option = {
        title: {
            text: 'Medicare Over Cities',
            subtext:'Aurin Data',
            left: 'center',
            textStyle: {
                fontSize: 20,
                color:"#44444b",
                fontFamily:"Comic Sans MS"
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                // Use axis to trigger tooltip
                type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
            }
        },
        legend: {top: 50},
        grid: {
            left: '3%',
            right: '4%',
            top: 100,
            containLabel: true
        },
        xAxis: {
            type: 'value'
        },
        yAxis: {
            type: 'category',
            data: ['Melbourne','Brisbane','Sydney']
        },
        series: [
            {
                name: 'Medicare Benefits Expenditure',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true
                },
                emphasis: {
                    focus: 'series'
                },
                data: [864.5,	820.25,	955]
            },
            {
                name: 'Number of Services (x10)',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true
                },
                emphasis: {
                    focus: 'series'
                },
                data: [156,150,170]
            },
            {
                name: 'Out-Of-Pocket Cost',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true
                },
                emphasis: {
                    focus: 'series'
                },
                data: [243, 247.5, 207]
            },

        ]
    };
    horbarChart = echarts.init(document.getElementById(id));
    option && horbarChart.setOption(option);
}

//aurin two side bar chart for suburb
function createTwoSideBar(id) {
    option = {
        title: {
            text: 'Disability Benefits Over Suburbs',
            subtext:'Aurin Data',
            left: 'center',
            textStyle: {
                fontSize: 20,
                color:"#44444b",
                fontFamily:"Comic Sans MS"
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        legend: {
            top: '15%',
            data: ['Female', 'Male']
        },
        grid: {
            left: '3%',
            right: '4%',
            top: '20%',
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
                    show: false
                },
                data: ['Darebin', 'Melbourne City', 'Port Phillip', 'Stonnington', 'Yarra']
            }
        ],
        series: [
            {
                name: 'Male',
                type: 'bar',
                stack: 'Total',
                label: {
                    show: true
                },
                emphasis: {
                    focus: 'series'
                },
                data: [1919, 2891, 3023, 1879, 2780]
            },
            {
                name: 'Female',
                type: 'bar',
                stack: 'Total',
                label: {
                    show: true,
                    position: 'left'
                },
                emphasis: {
                    focus: 'series'
                },
                data: [-2969, -4045, -4698, -2997, -4068]
            }
        ]
    };
    horbarChart = echarts.init(document.getElementById(id));
    option && horbarChart.setOption(option);
}