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



document.addEventListener('DOMContentLoaded', function () {
    const accordionButtons = document.querySelectorAll('.accordion-button');

    accordionButtons.forEach(button => {
        button.addEventListener('click', function () {
            const icon = this.querySelector('.arrow-icon');
            const target = document.querySelector(this.dataset.target);

            // Toggle the display of the target accordion content
            if (target.classList.contains('show')) {
                target.classList.remove('show');
                icon.classList.remove('rotate');
            } else {
                // Hide any other open accordion content
                document.querySelectorAll('.accordion-content').forEach(content => content.classList.remove('show'));
                document.querySelectorAll('.arrow-icon').forEach(icon => icon.classList.remove('rotate'));

                target.classList.add('show');
                icon.classList.add('rotate');
            }
        });
    });
});


