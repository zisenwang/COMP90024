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
        console.log(options)
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