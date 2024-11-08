 // define functions for two weeks graph
 function drawTwoWeekGraph(elementId) {
    const today = new Date();
    const twoWeeksAgo = new Date();
    twoWeeksAgo.setDate(today.getDate() - 14);
    const formatDate = date => date.toISOString().split('T')[0];
    fetch(`/api/detections/aggregates/?start=${formatDate(twoWeeksAgo)}&end=${formatDate(today)}&interval=day`)
        .then(response => response.json())
        .then(data => {
            const margin = { top: 40, right: 30, bottom: 60, left: 60 },
            width = 600 - margin.left - margin.right,
            height = 400 - margin.top - margin.bottom;
            const parseTime = d3.timeParse('%Y-%m-%d');
            const x = d3.scaleTime().range([0, width]);
            const y = d3.scaleLinear().range([height, 0]);
            const svg = d3.select(elementId)
                            .append("div")
                            // Container class to make it responsive.
                            .classed("svg-container", true) 
                            .append("svg")
                            // Responsive SVG needs these 2 attributes and no width and height attr.
                            .attr("preserveAspectRatio", "xMinYMin meet")
                            .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
                            // Class to make it responsive.
                            .classed("svg-content-responsive", true)
                            .append('g')
                            .attr('transform', `translate(${margin.left}, ${margin.top})`);
            // add title
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", 0 - (margin.top / 2))
                .attr("text-anchor", "middle")
                .style("font-size", "26px")
                .text("Detections in the Last Two Weeks");
            // Add Y axis label
            svg.append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 0 - margin.left)
                .attr("x", 0 - (height / 2))
                .attr("dy", "1em")
                .style("font-size", "20px")
                .style("text-anchor", "middle")
                .text("Number of Detections");
            // add tooltip
            const tooltip = d3.select("#detection-two-weeks")
                .append("div")
                .attr("class", "tooltip")
                .style("opacity", 0);
            // Add gradient definition after SVG creation
            const gradient = svg.append("defs")
                .append("linearGradient")
                .attr("id", "bar-gradient")
                .attr("x1", "0%")
                .attr("x2", "0%")
                .attr("y1", "100%")
                .attr("y2", "0%");
            gradient.append("stop")
                .attr("offset", "0%")
                .attr("style", "stop-color:#90caf9;stop-opacity:1");
            gradient.append("stop")
                .attr("offset", "100%")
                .attr("style", "stop-color:#1976d2;stop-opacity:1");
            // Parse the date and count
            data.forEach(d => {
                d.date = parseTime(d.timestamp);
                d.count = +d.count;
            });
            // Fill in missing dates with 0 count
            const dateSet = new Set(data.map(d => d.date.getTime()));
            for (let d = twoWeeksAgo; d <= today; d.setDate(d.getDate() + 1)) {
                if (!dateSet.has(d.getTime())) {
                    data.push({ date: new Date(d), count: 0 });
                }
            }
            // Sort data by date
            data.sort((a, b) => a.date - b.date);
            x.domain(d3.extent(data, d => d.date));
            y.domain([0, d3.max(data, d => d.count)]);
            // create x axis
            svg.append('g')
                .attr('transform', `translate(0, ${height})`)
                .call(d3.axisBottom(x)
                    .ticks(4)  // reduce number of ticks
                    .tickFormat(d3.timeFormat("%m/%d")))  // shorter date format
                .call(
                    g => {
                        g.select(".domain").remove();
                        g.selectAll(".tick line").remove();  // Remove tick marks
                    }
                )  // Remove the vertical line
                .selectAll("text")  
                .style("font-size", "20px")  // larger font size
                .style("text-anchor", "end")
                .attr("dx", "-.1em")
                .attr("dy", ".2em")
                .attr("transform", "rotate(-45)");  // rotate labels 45 degrees
            // create y axis
            svg.append('g')
                .call(d3.axisLeft(y)
                    .ticks(5))  // reduce number of ticks
                .call(
                    g => {
                        g.select(".domain").remove();
                        g.selectAll(".tick line").remove();  // Remove tick marks
                    }
                )  // Remove the vertical line
                .selectAll("text")
                .style("font-size", "20px");  // larger font
            // add horizontal grid lines
            svg.append('g')
                .attr('class', 'grid')
                .call(d3.axisLeft(y)
                    .ticks(5)
                    .tickSize(-width)  // Make lines span full width
                    .tickFormat('')  // No labels (already added above)
                )
                .style('stroke', '#e0e0e0')  // Light grey color
                .style('stroke-width', '2px')  // Increase stroke width
                .style('stroke-opacity', 0.1)
                .call(g => g.select(".domain").remove());  // Remove vertical line
            // add bars
            const bars = svg.selectAll('.bar')
                .data(data)
                .enter().append('rect')
                .attr('class', 'bar')
                .attr('x', d => x(d.date) - 15)
                .attr('y', height)
                .attr('width', 30) // Set a fixed width for the bars
                .attr('height', 0)  // Start with 0 height
                .attr('rx', 3)  // horizontal corner radius
                .attr('ry', 3)  // vertical corner radius
                .attr('fill', 'url(#bar-gradient)');
            
            // Add animation
            bars.transition()
                .duration(500)
                .delay((d, i) => i * 20)
                .attr('y', d => y(d.count))
                .attr('height', d => height - y(d.count));
            // add mouseover and mouseout events
            bars.on('mouseover', function(event, d) {
                    const screenCenter = window.innerWidth / 2;
                    const tooltipOffset = 10;

                    d3.select(this)
                        .transition()
                        .duration(200)
                        .style("fill", "#90caf9");
                    
                    tooltip.transition()
                        .duration(200)
                        .style("opacity", .9);
                        
                    tooltip.html(`Date: ${d3.timeFormat("%B %d, %Y")(d.date)}<br/>Count: ${d.count}`)
                    .style("left", (event.pageX > screenCenter ? 
                        (event.pageX - tooltip.node().offsetWidth - tooltipOffset) : 
                        (event.pageX + tooltipOffset)) + "px")
                    .style("top", (event.pageY - 28) + "px");
                });
            bars.on('mouseout', function() {
                    d3.select(this)
                        .transition()
                        .duration(500)
                        .style("fill", 'url(#bar-gradient)');
                        
                    tooltip.transition()
                        .duration(500)
                        .style("opacity", 0);
                });
        });
}

// define functions for 6 months graph
function drawSixMonthsGraph(elementId) {
    const today = new Date();
    const sixMonthsAgo = new Date();
    sixMonthsAgo.setMonth(today.getMonth() - 6);
    const formatDate = date => date.toISOString().split('T')[0];
    fetch(`/api/detections/aggregates/?start=${formatDate(sixMonthsAgo)}&end=${formatDate(today)}&interval=month`)
        .then(response => response.json())
        .then(data => {
            const margin = { top: 40, right: 30, bottom: 60, left: 90 },
            width = 600 - margin.left - margin.right,
            height = 400 - margin.top - margin.bottom;
            const parseTime = d3.timeParse('%Y-%m');
            const x = d3.scaleTime().range([0, width]);
            const y = d3.scaleLinear().range([height, 0]);
            const svg = d3.select(elementId)
                            .append("div")
                            // Container class to make it responsive.
                            .classed("svg-container", true) 
                            .append("svg")
                            // Responsive SVG needs these 2 attributes and no width and height attr.
                            .attr("preserveAspectRatio", "xMinYMin meet")
                            .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
                            // Class to make it responsive.
                            .classed("svg-content-responsive", true)
                            .append('g')
                            .attr('transform', `translate(${margin.left}, ${margin.top})`);
            // add title
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", 0 - (margin.top / 2))
                .attr("text-anchor", "middle")
                .style("font-size", "26px")
                .text("Detections in the Last Six Months");
            // Add Y axis label
            svg.append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 0 - margin.left)
                .attr("x", 0 - (height / 2))
                .attr("dy", "1em")
                .style("font-size", "20px")
                .style("text-anchor", "middle")
                .text("Number of Detections");
            // add tooltip
            const tooltip = d3.select("#detection-six-months")
                .append("div")
                .attr("class", "tooltip")
                .style("opacity", 0);
            // Add gradient definition after SVG creation
            const gradient = svg.append("defs")
                .append("linearGradient")
                .attr("id", "bar-gradient")
                .attr("x1", "0%")
                .attr("x2", "0%")
                .attr("y1", "100%")
                .attr("y2", "0%");
            gradient.append("stop")
                .attr("offset", "0%")
                .attr("style", "stop-color:#90caf9;stop-opacity:1");
            gradient.append("stop")
                .attr("offset", "100%")
                .attr("style", "stop-color:#1976d2;stop-opacity:1");
            // Parse the date and count
            data.forEach(d => {
                d.date = parseTime(d.timestamp);
                d.count = +d.count;
            });
            x.domain(d3.extent(data, d => d.date));
            y.domain([0, d3.max(data, d => d.count)]);
            // create x axis
            svg.append('g')
                .attr('transform', `translate(0, ${height})`)
                .call(d3.axisBottom(x)
                    .ticks(6)  // reduce number of ticks
                    .tickFormat(d3.timeFormat("%b %y")))  // shorter date format
                .call(
                    g => {
                        g.select(".domain").remove();
                        g.selectAll(".tick line").remove();  // Remove tick marks
                    }
                )  // Remove the vertical line
                .selectAll("text")  
                .style("font-size", "20px")  // larger font size
                .style("text-anchor", "end")
                .attr("dx", "-.1em")
                .attr("dy", ".2em")
                .attr("transform", "rotate(-45)");  // rotate labels 45 degrees
            // create y axis
            svg.append('g')
                .call(d3.axisLeft(y)
                    .ticks(5))  // reduce number of ticks
                .call(
                    g => {
                        g.select(".domain").remove();
                        g.selectAll(".tick line").remove();  // Remove tick marks
                    }
                )  // Remove the vertical line
                .selectAll("text")
                .style("font-size", "20px")
                .attr("dx", "-1.2em")  // Adjust text position
                .attr("dy", ".15em");
            // add horizontal grid lines
            svg.append('g')
                .attr('class', 'grid')
                .call(d3.axisLeft(y)
                    .ticks(5)
                    .tickSize(-width)  // Make lines span full width
                    .tickFormat('')  // No labels (already added above)
                )
                .style('stroke', '#e0e0e0')  // Light grey color
                .style('stroke-width', '2px')  // Increase stroke width
                .style('stroke-opacity', 0.1)
                .call(g => g.select(".domain").remove());  // Remove vertical line
            // add bars
            const bars = svg.selectAll('.bar')
                .data(data)
                .enter().append('rect')
                .attr('class', 'bar')
                .attr('x', d => x(d.date) - 30)
                .attr('y', height)
                .attr('width', 60) // Set a fixed width for the bars
                .attr('height', 0)  // Start with 0 height
                .attr('rx', 3)  // horizontal corner radius
                .attr('ry', 3)  // vertical corner radius
                .attr('fill', 'url(#bar-gradient)');
              // Add animation
              bars.transition()
              .duration(500)
              .delay((d, i) => i * 20)
              .attr('y', d => y(d.count))
              .attr('height', d => height - y(d.count));
          // add mouseover and mouseout events
          bars.on('mouseover', function(event, d) {
                  const screenCenter = window.innerWidth / 2;
                  const tooltipOffset = 10;

                  d3.select(this)
                      .transition()
                      .duration(200)
                      .style("fill", "#90caf9");
                  
                  tooltip.transition()
                      .duration(200)
                      .style("opacity", .9);
                      
                  tooltip.html(`Date: ${d3.timeFormat("%B %d, %Y")(d.date)}<br/>Count: ${d.count}`)
                  .style("left", (event.pageX > screenCenter ? 
                      (event.pageX - tooltip.node().offsetWidth - tooltipOffset) : 
                      (event.pageX + tooltipOffset)) + "px")
                  .style("top", (event.pageY - 28) + "px");
              });
          bars.on('mouseout', function() {
                  d3.select(this)
                      .transition()
                      .duration(500)
                      .style("fill", 'url(#bar-gradient)');
                      
                  tooltip.transition()
                      .duration(500)
                      .style("opacity", 0);
              });
      });
}
        