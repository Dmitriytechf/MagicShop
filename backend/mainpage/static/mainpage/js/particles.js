let particles = document.querySelectorAll('.particles'),
    radius = 3.9,
    number = 450;

particles.forEach(node => {
    let color = node.dataset.color;
    const ctx = node.getContext('2d'),
          clr = hexToRgbA(color),
          width = window.innerWidth,
          height = window.innerHeight;

    node.width = width;
    node.height = height;
    ctx.fillStyle = clr;

    let dots = {
        num: number,
        distance: 200,
        d_radius: 200,
        velocity: -.2,
        array: []
    };

    function Dot() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.vx = (dots.velocity + Math.random() * 0.3);
        this.vy = (dots.velocity + Math.random() * 0.3);
        this.radius = Math.random() * radius;
    }

    Dot.prototype = {
        create: function() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
            ctx.fill();
        },

        animate: function() {
            if (this.x < 0 || this.x > width) {
                this.vx = -this.vx;
            }
            if (this.y < 0 || this.y > height) {
                this.vy = -this.vy;
            }
            this.x += this.vx;
            this.y += this.vy;
        }
    };

    // Инициализация частиц
    for (let i = 0; i < dots.num; i++) {
        dots.array.push(new Dot());
    }

    function animateDots() {
        ctx.clearRect(0, 0, width, height);
        for (let i = 0; i < dots.num; i++) {
            dots.array[i].animate();
            dots.array[i].create();
        }
        requestAnimationFrame(animateDots);
    }

    animateDots();

    // Обработчик изменения размера окна
    window.addEventListener('resize', function() {
        node.width = window.innerWidth;
        node.height = window.innerHeight;
        width = node.width;
        height = node.height;
    });
});

function hexToRgbA(hex) {
    if (/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)) {
        let c = hex.substring(1).split('');
        if (c.length == 3) {
            c = [c[0], c[0], c[1], c[1], c[2], c[2]];
        }
        c = '0x' + c.join('');
        return 'rgba(' + [(c >> 16) & 255, (c >> 8) & 255, c & 255].join(',') + ',1)';
    }
    throw new Error('Bad Hex');
}