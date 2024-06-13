document.addEventListener('DOMContentLoaded', function() {
    const animation = document.getElementById('error-animation');
    
    function playAnimation() {
        animation.play();
        setTimeout(() => {
            animation.pause();
        }, 1850);
    }
    playAnimation();
});