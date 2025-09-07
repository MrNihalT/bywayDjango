document.addEventListener('DOMContentLoaded',()=>{
let mobilemenu = document.getElementById("mobileMenu"); 
let menubutton = document.getElementById("menuToggle");

menubutton.onclick = function () {
    console.log("Menu toggled");

    mobilemenu.classList.toggle("active");

   
};
document.addEventListener("click", function (e) {
    if (!mobilemenu.contains(e.target) && !menubutton.contains(e.target)) {
        mobilemenu.classList.remove("active");
    }
});


const scrollContainer = document.getElementById('review-list');
    const leftBtn = document.getElementById('scroll-left');
    const rightBtn = document.getElementById('scroll-right');

    // Make sure all elements exist before adding event listeners
    if (scrollContainer && leftBtn && rightBtn) {
        
        // Calculate the distance to scroll (the width of one card plus its margin)
        const scrollAmount = scrollContainer.querySelector('li').clientWidth + 24; // 24px is 1.5rem

        // When the right button is clicked...
         rightBtn.addEventListener('click',()=>{
            if (scrollContainer.scrollLeft+ scrollContainer.clientWidth >= scrollContainer.scrollWidth -1){
                scrollContainer.scrollLeft = 0;
            }else{
                scrollContainer.scrollLeft += scrollAmount;
            }
         })
         leftBtn.addEventListener('click',()=>{
            if(scrollContainer.scrollLeft<=0){
                scrollContainer.scrollLeft= scrollContainer.scrollWidth - scrollContainer.clientWidth;
            } else {
                scrollContainer.scrollLeft -= scrollAmount
            }
         })
    }
})
