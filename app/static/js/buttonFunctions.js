function getState() {
  const htmlBoard = document.getElementById("cardgrid").querySelectorAll(".empty-slot");
  let board = [];
  htmlBoard.forEach((slot) => {
    let htmlCards = slot.querySelectorAll(".card");
    let cards = [];
    htmlCards.forEach((card) => {
      let url = card.dataset.imgUrl;
      url = url.replace("url(static/images/", "").replace(".svg)", "").split("-");
      let suit = url[0];
      let points = url[1];
      let name;
      if (points == "1" || Number(points) > 10) {
        name = url[2];
      }
      else {
        name = "N" + points;
      }
      let cardJson = {
        "name": name,
        "suit": suit,
        "status": card.dataset.status
      };
      cards.push(cardJson);
    });
    if (cards.length != 0) {
      board.push(cards);
    }
    else {
      board.push(null);
    }
  });

  const playerHand = document.getElementById("player-hand");
  let htmlHand= playerHand.querySelectorAll(".card");
  let hand = [];
  htmlHand.forEach((card) => {
    let url = card.dataset.imgUrl;
    url = url.replace("url(static/images/", "").replace(".svg)", "").split("-");
    let suit = url[0];
    let points = url[1];
    let name;
    if (points == "1" || Number(points) > 10) {
      name = url[2];
    }
    else {
      name = "N" + points;
    }
    let cardJson = {
      "name": name,
      "suit": suit,
      "status": card.dataset.status
    };
    hand.push(cardJson);
  });
  return {
    hand,
    board
  };
}

async function sortCardsInHand() {
  let state = getState();
  await fetch('/sort-cards', {
    method: "POST",
    body: JSON.stringify({
      cards: state.hand
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  });
}

async function showStack() {
  try {
    let state = getState();
    await fetch('/show-stack', {
      method: "POST",
      body: JSON.stringify({
        board: state.board
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    });
  }
  catch (error) {
    console.log("Load failed!***" + error);
  } 
}

async function updateState() {
  try {
    let state = getState();
    await fetch('/update-state', {
      method: "POST",
      body: JSON.stringify(state),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    });
  }
  catch (error) {
    console.log("Load failed!***" + error);
  }
}

// Add listeners to buttons
const sortCardsInHandBtn = document.getElementById('sort-cards-in-hand-btn');
sortCardsInHandBtn.addEventListener("click", async (event) => {
  await sortCardsInHandBtn();
  window.location.reload();
});

const doneBtn = document.getElementById('done-btn');
doneBtn.addEventListener("click", async (event) => {
  await updateState();
  window.location.reload();
});

const showStackBtn = document.getElementById('show-stack-btn');
showStackBtn.addEventListener("click", async (event) => {
  await showStack();
  window.location.reload();
});

console.log((showStackBtn))