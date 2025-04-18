const slider = document.querySelector('.slider');
const sliderControl = document.querySelector('.sliderControl');
let scrollAdress = 0;

let controlButtons = Array.from(document.querySelectorAll('.controlButton'));

const delClass = () => {
    controlButtons.forEach(button => {
        button.classList.remove('active');
    })
}

const addClass = (button) => {
    button.classList.add('active');
} 
 
controlButtons.forEach(button => {
    button.addEventListener('click', function(event) {
        slider.scrollLeft = slider.clientWidth * (controlButtons.indexOf(button));
        delClass();
        addClass(controlButtons[controlButtons.indexOf(button)]);
    })
    
});

const getSlide = () => {
    const scrollPosition = slider.scrollLeft; 
    const slideWidth = slider.clientWidth; 
    const currentSlide = Math.round(scrollPosition / slideWidth); 
    return currentSlide + 1;
}

slider.addEventListener('scroll', () => {  
    scrollAdress = scrollAdress === getSlide() ? scrollAdress : getSlide();
    delClass();
    addClass(controlButtons[scrollAdress - 1]);



    switch (true) {
        case (scrollAdress >= 1 && scrollAdress <= 6):
            sliderControl.scrollLeft = sliderControl.clientWidth * 0;
            break;
        case (scrollAdress >= 7 && scrollAdress <= 12):
            sliderControl.scrollLeft = sliderControl.clientWidth * 1;
            break;
        case (scrollAdress >= 13 && scrollAdress <= 18):
            sliderControl.scrollLeft = sliderControl.clientWidth * 2;
            break;
        default:
            break;
    }
});




/*const openPopupBtn = document.getElementById('openPopupBtn');*/
const openPopupBtns = document.querySelectorAll('#openPopupBtn');
const overlay = document.getElementById('overlay');
const popup = document.getElementById('popup');
const closePopupBtn = document.getElementById('closePopupBtn');
const submitButton = document.querySelector('.submit-btn');

submitButton.addEventListener('click', async function(event) {
    overlay.style.display = 'none'; 

    let card = event.target.closest('.popup');
    let date = overlay.querySelector("#popup > div.placeBlock > div > p.placeBlockName").getAttribute("datevalue");
    let pairIndex = overlay.querySelector("#popup > div.placeBlock > div > p.placeBlockName").getAttribute("pairindex");
    let pairName = card.querySelector("#popup > div.placeBlock > div > p.placeBlockName").textContent;
    let dz = card.querySelector("#inputText").value;

    const transmitData = {
        "date": date, 
        "pairindex": pairIndex,
        "pairname": pairName,
        "homework": dz
    };
    
    try {
        const response = await fetch("http://127.0.0.1:5000/api/endpoint", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(transmitData),
        });
    } catch (error) {
        //
    }
})

openPopupBtns.forEach(openPopupBtn => {
    openPopupBtn.addEventListener('click', function(event) {

        overlay.style.display = 'block'; 
        let pairValue = event.target.closest('.pair');
        let cab = pairValue.querySelector('.infoblock .meetInfoBlock .cabname').textContent;
        let pairType = pairValue.querySelector('.infoblock .meetInfoBlock .typePair').textContent;
        let pairIndex = pairValue.querySelector("div.dateblock > p").textContent[0];
        let dateValue = pairValue.querySelector("div.dateblock > p").getAttribute("date");
        let pairName = pairValue.querySelector('.infoblock .dzblock .predmet').textContent;
        let dz = pairValue.querySelector('.infoblock .dzblock .getDataDz').textContent;

        const block = document.querySelector("#popup > div.placeBlock > p");
        block.innerHTML = block.innerHTML.replace(/^\d+x/, cab);
        overlay.querySelector("#popup > div.placeBlock > p > span").textContent = pairType;
        overlay.querySelector("#popup > div.placeBlock > div > p.placeBlockName").textContent = pairName;
        overlay.querySelector("#popup > div.placeBlock > div > p.placeBlockName").setAttribute("pairindex", String(pairIndex));
        overlay.querySelector("#popup > div.placeBlock > div > p.placeBlockName").setAttribute("datevalue", String(dateValue));
        overlay.querySelector("#inputText").value = dz;
        
    });
});


overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
        overlay.style.display = 'none'; 
    }
});

closePopupBtn.addEventListener('click', () => {
    overlay.style.display = 'none'; 
});
