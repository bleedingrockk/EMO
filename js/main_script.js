document.getElementById('container3_heading_1').addEventListener('click', function() {
    var target1 = document.getElementById('container4_sub1_1');
    target1.style.display = 'block'; 
    var target2 = document.getElementById('container4_sub1_2');
    target2.style.display = 'none'; 
    var target3 = document.getElementById('container4_sub1_3');
    target3.style.display = 'none'; 
});

document.getElementById('container3_heading_2').addEventListener('click', function() {
    var target1 = document.getElementById('container4_sub1_1');
    target1.style.display = 'none'; 
    var target2 = document.getElementById('container4_sub1_2');
    target2.style.display = 'block'; 
    var target3 = document.getElementById('container4_sub1_3');
    target3.style.display = 'none'; 
});

document.getElementById('container3_heading_3').addEventListener('click', function() {
    var target1 = document.getElementById('container4_sub1_1');
    target1.style.display = 'none'; 
    var target2 = document.getElementById('container4_sub1_2');
    target2.style.display = 'none'; 
    var target3 = document.getElementById('container4_sub1_3');
    target3.style.display = 'block'; 
});