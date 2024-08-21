document.addEventListener("DOMContentLoaded", () => {
    let selectedCard = null;
    /*
    function onCardClick(event) {
        console.log("Card click!");
        // Deselect previously selected card if any
        if (selectedCard === event.target) {
            // Deselect the card
            selectedCard.classList.remove("selected");
            selectedCard = null; // Clear the selection
        }
        else {
            console.log("Selected:");
            console.log(selectedCard);
            console.log("Target:")
            console.log(event.target);
            if (selectedCard != null) {
                selectedCard.classList.remove("selected");
                selectedCard = null;
            }
            else {
                // Select the clicked card
                selectedCard = event.target;
                selectedCard.classList.add("selected");
            }
        }
    }
    */
    function onCardClick(event) {
        console.log("Card click!");
        // Deselect previously selected card if any
        if (selectedCard === event.target) {
            // Deselect the card
            selectedCard.classList.remove("selected");
            selectedCard = null; // Clear the selection
        }
        else {
            console.log("Selected:");
            console.log(selectedCard);
            console.log("Target:")
            console.log(event.target);
            if (selectedCard != null) {
                selectedCard.classList.remove("selected");
                selectedCard = null;
            }
            else {
                // Select the clicked card
                selectedCard = event.target;
                selectedCard.classList.add("selected");
            }
        }
    }
    // Function to handle empty slot click
    function onEmptySlotClick(event) {
        console.log("Slot clicked!")
        if (selectedCard === event.target) {
            // Deselect the card
            selectedCard.classList.remove("selected");
            selectedCard = null; // Clear the selection
        }
        else {
            if (selectedCard) {
                // Clone the selected card and append it to the empty slot
                isNotTopCard = event.target.querySelector(".card");
                if (isNotTopCard) return;

                targetParentSlot = event.target.closest(".empty-slot");
                selectedCardParentSlot = selectedCard.closest(".empty-slot");

                if (targetParentSlot === selectedCardParentSlot) return;

                const cardClone = selectedCard.cloneNode(true);
                cardClone.classList.remove("selected");
                event.target.appendChild(cardClone);

                // Remove the selected class from the original card
                selectedCard.classList.remove("selected");
                selectedCard.remove()
                selectedCard = null;
            }
            else {
                // Select the clicked card
                if (event.target.classList.contains("card")) {
                    selectedCard = event.target;
                    selectedCard.classList.add("selected");                }
            }
        }
    }

    // Function to handle empty slot click
    function onHandClick(event) {
        console.log("Hand clicked!");
        console.log("Selected:")
        console.log(selectedCard)
        console.log("Event:")
        console.log(event.target);
        console.log(selectedCard == event.target);
        if (selectedCard == event.target) {
            selectedCard.classList.remove("selected");
            selectedCard = null;
        }
        else if (selectedCard) {
            isCardInHand = selectedCard.parentElement.classList.contains("small-hand");
            if (isCardInHand) return;
            // Clone the selected card and append it to the empty slot

            isNotTopCard = selectedCard.querySelector(".card");
            let stackedCards;
            if (isNotTopCard) {
                stackedCards = selectedCard.querySelectorAll(".card");         
                let playerHand = document.getElementById("player-hand");
                let stackedCardClone;
                for (let i=stackedCards.length-1; i >= 0; i--) {
                    stackedCardClone = stackedCards[i].cloneNode(true);
                    playerHand.appendChild(stackedCardClone);
                    stackedCards[i].remove();
                }
                const selectCardClone = selectedCard.cloneNode(true);
                selectCardClone.classList.remove("selected");
                playerHand.appendChild(stackedCardClone);
                selectedCard.remove();
                return;
            }

            const cardClone = selectedCard.cloneNode(true);
            cardClone.classList.remove("selected");

            handContainer = event.target.querySelector(".small-hand");
            if (handContainer) {
                handContainer.appendChild(cardClone);
            }
            else { // fix: event target was small-hand instead of small-hand-container
                event.target.appendChild(cardClone);
            }

            // Remove the selected class from the original card
            selectedCard.classList.remove("selected");
            selectedCard.remove();
            selectedCard = null;
        }
        else {
            // Select the clicked card
            //remove selected
            if (event.target.classList.contains("card")) {
                selectedCard = event.target;
                selectedCard.classList.add("selected");
            }
        }
    }

    function onFlipCardBtnClick(event) {
        console.log("Btn clicked!");
        if (selectedCard) {
            let currentBgImgUrl = selectedCard.style.backgroundImage;
            for (let i = 0; i < 2; i++) {
                currentBgImgUrl = currentBgImgUrl.replace('"', '');
            }
            if (
                currentBgImgUrl === selectedCard.dataset.imgUrl
            ) {
                selectedCard.style.backgroundImage = "url(static/images/CARD-CLOSED.svg)";
                selectedCard.dataset.status = 0;
            }
            else {
                selectedCard.style.backgroundImage = selectedCard.dataset.imgUrl;
                selectedCard.dataset.status = 1;
            }
            selectedCard.classList.remove("selected");
            selectedCard = null;
        }
    }

    function flipAllCardsInHand(event) {
        playerHand = document.getElementById("player-hand");
        playerCards = playerHand.querySelectorAll(".card");
        let currentBgImgUrl;
        playerCards.forEach(card => {
            currentBgImgUrl = card.style.backgroundImage;
            for (let i = 0; i < 2; i++) {
                currentBgImgUrl = currentBgImgUrl.replace('"', '');
            }
            if (
                currentBgImgUrl === card.dataset.imgUrl
            ) {
                card.style.backgroundImage = "url(static/images/CARD-CLOSED.svg)";
                card.dataset.status = 0;
            }
            else {
                card.style.backgroundImage = card.dataset.imgUrl;
                card.dataset.status = 1;
            }
        });
    }

    function putAllCardsInHand(event) {
        cardGrid = document.getElementById("cardgrid");
        playerHand = document.getElementById("player-hand");
        allGridcards = cardGrid.querySelectorAll(".card");
        let cardClone;
        for (let i=allGridcards.length-1; i >= 0; i--) {
            cardClone = allGridcards[i].cloneNode(true);
            playerHand.appendChild(cardClone);
            allGridcards[i].remove();
        }
    }

    // Attach click event listeners to all cards
    /*
    let cards = document.querySelectorAll(".card");
    cards.forEach(card => {
        card.addEventListener("click", onCardClick);
    });
    */

    // Attach click event listeners to all empty slots
    let emptySlots = document.querySelectorAll(".empty-slot");
    emptySlots.forEach(slot => {
        slot.addEventListener("click", onEmptySlotClick);
    });

    // Attach click event listeners to hands
    let hands = document.querySelectorAll(".small-hand-container");
    hands.forEach(hand => {
        hand.addEventListener("click", onHandClick);
    });

    const flipBtn = document.getElementById("flip-card-btn");
    flipBtn.addEventListener("click", onFlipCardBtnClick);

    const flipAllCardsInHandBtn = document.getElementById("flip-cards-in-hand-btn");
    flipAllCardsInHandBtn.addEventListener("click", flipAllCardsInHand);

    const putAllCardsInHandBtn = document.getElementById("put-card-in-hand-btn");
    putAllCardsInHandBtn.addEventListener("click", putAllCardsInHand);
});
