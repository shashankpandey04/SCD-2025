const canvas = document.getElementById('animated-bg-canvas');
const ctx = canvas.getContext('2d');
let circles = [];

function resizeCanvas() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

function randomColor() {
    const colors = [
        'rgba(139,92,246,0.15)',
        'rgba(34,197,94,0.12)',
        'rgba(59,130,246,0.12)',
        'rgba(244,63,94,0.12)',
        'rgba(251,191,36,0.10)'
    ];
    return colors[Math.floor(Math.random() * colors.length)];
}

function createCircle() {
    const radius = Math.random() * 60 + 40;
    return {
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: radius,
        color: randomColor(),
        speed: Math.random() * 0.6 + 0.3,
        dx: (Math.random() - 0.5) * 0.5
    };
}

function initCircles() {
    circles = [];
    for (let i = 0; i < 18; i++) {
        circles.push(createCircle());
    }
}
initCircles();

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let c of circles) {
        ctx.beginPath();
        ctx.arc(c.x, c.y, c.r, 0, Math.PI * 2);
        ctx.fillStyle = c.color;
        ctx.fill();
        c.y -= c.speed;
        c.x += c.dx;
        if (c.y + c.r < 0 || c.x + c.r < 0 || c.x - c.r > canvas.width) {
            Object.assign(c, createCircle());
            c.y = canvas.height + c.r;
        }
    }
    requestAnimationFrame(animate);
}
animate();

window.addEventListener('resize', () => {
    resizeCanvas();
    initCircles();
});